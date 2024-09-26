import argparse
import os
import subprocess
import random

# Pull the github repository that was listed in the actions.
# Pull this into the apps folder.
# Supply docker compose with environment variables and files if needed
# Find an available port for each container
# replace ports in nginx.conf file
# Symlink the nginx.conf file to the sites-available folder with repo name.
# Run the docker compose command within the directory
# Restart nginx


parser = argparse.ArgumentParser(description="Quick and easy deploy")
parser.add_argument("--repo", action="store")
parser.add_argument("--name", action="store")

args = parser.parse_args()
port_range = (1, 65535)
app = os.path.expanduser(f"~/code/hosted/{args.name}")
conf_location = "/etc/nginx/sites-available"


def used_ports():
    command = "ss -tuln | awk '{print $5}' | cut -d':' -f2 | sort -u"
    result = subprocess.run(command, capture_output="True", text=True, shell=True)
    used = []
    for line in result.stdout.split("\n"):
        if line == "":
            continue
        if line == " ":
            continue
        if line == "Local":
            continue
        used.append(int(line.strip()))

    return used


def get_port():
    while True:
        port = random.randint(port_range[0], port_range[1])
        if port not in used_ports():
            return port


def git_pull():
    command = ["git", "pull"]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)


def replace_nginx():
    new_lines = []
    ports = []
    with open("nginx.conf", "r") as file:
        for line in file.readlines():
            if "%s" in line:
                port = get_port()
                ports.append(port)
                new_lines.append(line % (port))
            else:
                new_lines.append(line)

    with open("filled_nginx.conf", "w") as file:
        file.writelines(new_lines)

    return ports


def create_dotenv(ports):
    with open(".env", "w") as file:
        for count, port in enumerate(ports, start=1):
            file.write(f"PORT{count}={port}\n")


def symlink_nginx():
    nginx_abs = os.path.join(app, "filled_nginx.conf")
    available = f"/etc/nginx/sites-available/{args.name}"
    enabled = f"/etc/nginx/sites-enabled/{args.name}"

    os.symlink(nginx_abs, available)
    os.symlink(available, enabled)


def restart_nginx():
    try:
        subprocess.run(["sudo", "systemctl", "reload", "nginx"], check=True)
        print("NGINX reloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to reload NGINX: {e}")


def main():
    os.chdir(app)
    git_pull()
    ports = replace_nginx()
    create_dotenv(ports)
    symlink_nginx()
    restart_nginx()

main()
