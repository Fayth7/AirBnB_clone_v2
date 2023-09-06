#!/usr/bin/python3
"""
Compress and deploy web static package to remote servers.
"""

from fabric.api import *
from os import path

env.hosts = ['54.172.92.53', '34.207.61.123']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """
    Deploy web files to server.
    Args:
        archive_path (str): The path to the compressed archive file.
    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if not path.exists(archive_path):
        return False

    try:
        # Upload archive to server
        put(archive_path, '/tmp/')

        # Extract archive and delete .tgz
        timestamp = archive_path.split('_')[-1][:-4]
        release_dir = '/data/web_static/releases/web_static_{}'.format(
            timestamp)
        run('sudo mkdir -p {}'.format(release_dir))
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C {}'.format(timestamp, release_dir))
        run('sudo rm /tmp/web_static_{}.tgz'.format(timestamp))

        # Move contents into host web_static
        run('sudo mv {}/web_static/* {}/'.format(release_dir, release_dir))

        # Remove extraneous web_static dir
        run('sudo rm -rf {}/web_static'.format(release_dir))

        # Delete pre-existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Create a symbolic link
        run('sudo ln -s {} /data/web_static/current'.format(release_dir))

        return True
    except Exception as e:
        print(e)
        return False
