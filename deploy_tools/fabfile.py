from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/denizen-ru/superlists.git'


def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folser = site_folder + '/source'
    _create_directory_structure_if_nesseccery(site_folder)
    _get_latest_source(source_folser)
    _update_settings(source_folser, env.host)
    _update_virtualenv(source_folser)
    _update_static_files(source_folser)
    _update_database(source_folser)


def _create_directory_structure_if_nesseccery(site_folder):
    for subfolder in ('datebase', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folser):
    if exists(source_folser + '/.git'):
        run('cd %s && git fetch' % (source_folser,))
    else:
        run('git clone %s %s' % (REPO_URL, source_folser))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (source_folser, current_commit))


def _update_settings(source_folser, site_name):
    settings_path = source_folser + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 'DOMAIN = "localhost"', 'DOMAIN = "%s"' % (site_name,))
    secret_key_file = source_folser + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz01234567890!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folser):
    virtualenv_folder = source_folser + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/requirements.txt' %
        (virtualenv_folder, source_folser))


def _update_static_files(source_folser):
    run('cd %s && ../virtualenv/bin/python manage.py collectstatic --noinput' %
        (source_folser,))


def _update_database(source_folser):
    run('cd %s && ../virtualenv/bin/python manage.py migrate --noinput' %
        (source_folser,))


def _get_base_folder(host):
    return '~/sites/' + host


def _get_manage_dot_py(host):
    return '{path}/virtualenv/bin/python {path}/source/manage.py'.format(
        path=_get_base_folder(host)
    )


def reset_database():
    run('{manage_py} flush --noinput'.format(
        manage_py=_get_manage_dot_py(env.host)))


def create_session_on_server(email):
    session_key = run('{manage_py} create_session {email}'.format(
        manage_py=_get_manage_dot_py(env.host),
        email=email,
    ))
    print(session_key)
