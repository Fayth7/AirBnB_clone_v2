#!/usr/bin/env python3
"""
Fabric script to distribute an archive to your web servers and deploy it
"""

from fabric.api import run, put, env
from os.path import exists

# Replace with your actual server IPs
env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'  # Replace with your SSH username
# Replace with your SSH private key path
env.key_filename = 'my_ssh_private_key'


def do_deploy(archive_path):
    """Distribute and deploy an archive to the web servers"""

    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ on the remote server
        put(archive_path, '/tmp/')

        # Extract the archive to the appropriate folder
        archive_filename = archive_path.split('/')[-1]
        folder_name = "/data/web_static/releases/{}".format(
            archive_filename.split('.')[0])
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, folder_name))

        # Delete the archive from the remote server
        run("rm /tmp/{}".format(archive_filename))

        # Move the contents of the extracted folder to the web_static folder
        run("mv {}/web_static/* {}".format(folder_name, folder_name))

        # Remove the now empty web_static folder
        run("rm -rf {}/web_static".format(folder_name))

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the deployed version
        run("ln -s {} /data/web_static/current".format(folder_name))

        print("New version deployed!")
        return True

    except Exception as e:
        return False
