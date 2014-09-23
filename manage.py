#!/usr/bin/env python
import os, sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FuzzEd.settings')

    if "DJANGO_CONFIGURATION" not in os.environ:
    	# Not set by user, so we assume developer mode, since
    	# production systems are supposed to not use this script
    	os.environ["DJANGO_CONFIGURATION"]="Dev"
    	print("Assuming Dev mode")

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)