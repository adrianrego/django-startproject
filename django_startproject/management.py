from django_startproject import utils
import optparse
import os
import shutil
import subprocess
import sys


TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.realpath(utils.__file__)),
                            'project_template')


def start_project():
    """
    Copy a project template, replacing boilerplate variables.
    """
    usage = "usage: %prog [options] project_name [base_destination_dir]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-t', '--template-dir', dest='src_dir',
                      help='project template directory or repository to use',
                      default=TEMPLATE_DIR)
    options, args = parser.parse_args()
    if len(args) not in (1, 2):
        parser.print_help()
        sys.exit(1)
    project_name = args[0]

    src = options.src_dir

    if len(args) > 1:
        base_dest_dir = args[1]
    else:
        base_dest_dir = ''
    dest = os.path.join(base_dest_dir, project_name)

    # Detect and clone repo
    repo_info = src.split('+')
    tmp_dest = None

    if len(repo_info) > 1:
        vcs, url = repo_info
        tmp_dest = 'djstartproject_tmp_%s' % dest
        fnull = open(os.devnull, 'w')
        print "Cloning template from %s" % url
        subprocess.call([vcs, 'clone', url, tmp_dest], stdout = fnull, stderr = fnull)
        src = tmp_dest

    # Get any boilerplate replacement variables:
    replace = {}
    for var, help, default in utils.get_boilerplate(src, project_name):
        help = help or var
        if default is not None:
            prompt = '%s [%s]: ' % (help, default)
        else:
            prompt = '%s: ' % help
        value = None
        while not value:
            value = raw_input(prompt) or default
        replace[var] = value

    utils.copy_template(src, dest, replace)

    # Cleanup repo clone
    if tmp_dest != None:
        shutil.rmtree(tmp_dest)
