#!/usr/bin/python3
"""contains a Fabric script that generates a .tgz archive"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        (str): Archive path if generated correctly, otherwise None.
    """

    local("mkdir -p versions")

    now = datetime.utcnow()
    date_time = now.strftime("%Y%m%d%H%M%S")

    filename = "versions/web_static_{}.tgz".format(date_time)

    result = local("tar -cvzf {} web_static".format(filename))

    if result.succeeded:
        return filename
    else:
        return None
