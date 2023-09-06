#!/usr/bin/env python3
"""
Fabric script to clean out-of-date archives
"""

from fabric.api import run, local, env
from os.path import exists
from operator import itemgetter

# Replace with your actual server IPs
env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'  # Replace with your SSH username
# Replace with your SSH private key path
env.key_filename = 'my_ssh_private_key'


def do_clean(number=0):
    """Delete out-of-date archives"""

    number = int(number)
    if number < 0:
        number = 0

    try:
        # List all archives in the versions folder
        archives_local = local("ls -1tr versions", capture=True).split('\n')
        archives_remote = run(
            "ls -1tr /data/web_static/releases", capture=True).split('\n')

        # Keep only the most recent 'number' archives
        archives_to_keep_local = archives_local[-number:]
        archives_to_keep_remote = archives_remote[-number:]

        for archive in archives_local:
            if archive not in archives_to_keep_local:
                local("rm versions/{}".format(archive))

        for archive in archives_remote:
            if archive not in archives_to_keep_remote:
                run("rm /data/web_static/releases/{}".format(archive))

        return True

    except Exception as e:
        return False
