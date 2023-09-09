#!/usr/bin/python3
'''Fabric script to generate .tgz archive'''

from fabric.api import local
from datetime import datetime
from fabric.decorators import runs_once


@runs_once
def do_pack():
    '''Generates .tgz archive from the contents of the web_static folder'''
    try:
        local("mkdir -p versions")
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(current_time)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None


if __name__ == "__main__":
    result = do_pack()
    if result:
        print("Packaged: {}".format(result))
    else:
        print("Packaging failed")
