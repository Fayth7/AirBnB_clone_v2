#!/usr/bin/python3
"""
Fabric script to clean out-of-date archives and deploy web_static files.
"""

# Import necessary modules
from fabric.api import run, local, env, runs_once
from os.path import exists
from datetime import datetime
import os

# Set the list of remote hosts and the remote user
env.hosts = ['54.172.92.53', '34.207.61.123']
env.user = 'ubuntu'


@runs_once
def do_pack():
    """
    Archives the static files.

    Returns:
        str: The path to the archived static files, or None on failure.
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archive_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archive_size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """
    Deploys the static files to the host servers.

    Args:
        archive_path (str): The path to the archived static files.

    Returns:
        bool: True on successful deployment, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    success = False
    try:
        # Upload the archive
        put(archive_path, "/tmp/{}".format(file_name))
        
        # Create target directory
        run("mkdir -p {}".format(folder_path))
        
        # Uncompress archive and delete .tgz
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        
        # Move contents into host web_static
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        
        # Remove pre-existing symbolic link
        run("rm -rf /data/web_static/current")
        
        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success


def deploy():
    """
    Archives and deploys the static files to the host servers.

    Returns:
        bool: True on successful deployment, False otherwise.
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False


def do_clean(number=0):
    """
    Deletes out-of-date archives of the static files.

    Args:
        number (int): The number of archives to keep.
    """
    archives = os.listdir('versions/')
    archives.sort(reverse=True)
    start = int(number)
    if not start:
        start += 1
    if start < len(archives):
        archives = archives[start:]
    else:
        archives = []
    for archive in archives:
        os.unlink('versions/{}'.format(archive))
    cmd_parts = [
        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
        " '/data/web_static/releases/web_static_.*'",
        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1)
    ]
    run(''.join(cmd_parts))
