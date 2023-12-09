#!/usr/bin/python3
"""a Fabric script (based on the that creates and distributes an
   archive to your web servers, using the function deploy
"""

from fabric import task, Connection
from datetime import datetime

env.hosts = ['54.90.26.239', '184.72.101.54']


def do_pack():
    """
    Creates a compressed .tgz file from the contents of the
    web_static folder
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    local("mkdir -p versions")
    path = "versions/web_static_{}.tgz".format(timestamp)
    result = local("tar -cvzf {} web_static".format(path))
    if result.failed:
        return None
    return path


@task
def deploy(c):
    """
    Packs and deploys the web_static folder to web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    for host in env.hosts:
        with Connection(host) as conn:
            conn.put(archive_path, '/tmp/')
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            release_folder = "/data/web_static/releases/web_static_{}/"
            .format(timestamp)
            conn.run('mkdir -p {}'.format(release_folder))
            conn.run('tar -xzf /tmp/web_static_{}.tgz -C {}'
                     .format(timestamp, release_folder))
            conn.run('rm /tmp/web_static_{}.tgz'.format(timestamp))
            conn.run('mv {}web_static/* {}'.format(release_folder,
                                                   release_folder))
            conn.run('rm -rf {}web_static'.format(release_folder))
            conn.run('rm -rf /data/web_static/current')
            conn.run('ln -s {} /data/web_static/current'
                     .format(release_folder))
    return True
