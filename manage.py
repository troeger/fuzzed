#!/usr/bin/env python
import os, sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FuzzEd.settings')

    from configurations.management import execute_from_command_line

    if "runserver" in sys.argv:
        if "DJANGO_CONFIGURATION" not in os.environ:
            # Not set by Ansible Vagrant provisioning, so we assume developer mode, since
            # production systems are supposed to not use this script
            os.environ["DJANGO_CONFIGURATION"]="Dev"
            print("Assuming Dev mode")
            args = ["./manage.py","runserver","--configuration=Dev"]
            execute_from_command_line(args)
        else:
            os.environ["DJANGO_CONFIGURATION"]="Vagrant"
            print("Assuming Vagrant mode")
            args = ["./manage.py","runserver","192.168.33.10:8000","--configuration=Vagrant"]
            print "-------------------------------------------------------------------"
            print "Hint: You can reach this server from http://vagrant.fuzzed.org:8000"
            print "-------------------------------------------------------------------"
            execute_from_command_line(args)
    else:
        # Perform ordinary manage.py functionality
        execute_from_command_line(sys.argv)
