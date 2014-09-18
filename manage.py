#!/usr/bin/env python
import os, sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FuzzEd.settings')

    if "DJANGO_CONFIGURATION" not in os.environ:
        print "Please set the DJANGO_CONFIGURATION environment variable to either 'Dev', 'Vagrant' or 'Production'."
        exit(-1)

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)