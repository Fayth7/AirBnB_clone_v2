#!/usr/bin/env python3
"""
Fabric script to generate a .tgz archive from the web_static folder
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """Generates a .tgz archive from the web_static folder"""

    # Create the 'versions' directory if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Generate the name of the archive based on the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(timestamp)

    # Create the .tgz archive using 'tar'
    result = local("tar -cvzf {} web_static".format(archive_name))

    # Check if the archive was created successfully
    if result.failed:
        return None

    return archive_name
