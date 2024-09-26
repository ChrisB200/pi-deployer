import argparse
import subprocess

# Pull the github repository that was listed in the actions.
# Pull this into the apps folder.
# Supply docker compose with environment variables and files if needed
# Find an available port for each container
# replace ports in nginx.conf file
# Symlink the nginx.conf file to the sites-available folder with repo name.
# Run the docker compose command within the directory
# Restart nginx

apps = "~/code/apps"
conf_location = "/etc/nginx/sites-available"

parser = argparse.ArgumentParser(description="Quick and easy deploy")
parser.add_argument("--repo", action="store")
parser.add_argument("--name", action="store")

port_range = (1, 65535)


def find_ports():
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
    print(used)

find_ports()
