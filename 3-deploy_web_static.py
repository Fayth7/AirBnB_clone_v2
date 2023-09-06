#!/usr/bin/env python3
"""
Fabric script to create and distribute an archive to your web servers
"""

from fabric.api import local, run, put, env
from os.path import exists
from datetime import datetime

# Replace with your actual server IPs
env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'  # Replace with your SSH username
# Replace with your SSH private key path
env.key_filename = 'my_ssh_private_key'


def do_pack():
    """Generates a .tgz archive from the web_static folder"""

    # Create the 'versions' directory if it doesn't exist
    if not exists("versions"):
        local("mkdir -p versions")

    # Generate the name of the archive based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(timestamp)

    # Create the .tgz archive using 'tar'
    result = local("tar -cvzf {} web_static".format(archive_name))

    # Check if the archive was created successfully
    if result.failed:
        return None

    return archive_name


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


def deploy():
    """Create and distribute an archive, and deploy it to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
