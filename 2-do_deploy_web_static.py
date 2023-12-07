#!/usr/bin/python3
"""a Fabric script (based on the file 1-pack_web_static.py)
"""

from fabric.api import *
import os

env.hosts = ["<web-01 IP>", "<web-02 IP>"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers and deploys it.

    Args:
        archive_path (str): Path to the archive file.

    Returns:
        bool: True if all operations have been done correctly, otherwise False.
    """

    if not os.path.exists(archive_path):
        return False

    archive_name = os.path.basename(archive_path)
    archive_folder = "/data/web_static/releases/" + archive_name[:-4]

    try:
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(archive_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_name,
                                            archive_folder))
        run("sudo rm /tmp/{}".format(archive_name))
        run("sudo mv {}/web_static/* {}".format(archive_folder,
                                                archive_folder))
        run("sudo rm -rf {}/web_static".format(archive_folder))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".
            format(archive_folder))
        return True
    except Exception:
        return False
