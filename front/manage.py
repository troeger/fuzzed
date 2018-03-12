#!/usr/bin/env python3
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FuzzEd.settings')

    from configurations.management import execute_from_command_line

    if "runserver" in sys.argv:
        if os.environ["DJANGO_CONFIGURATION"] == "Dev":
            print("Assuming Dev mode")
            args = ["./manage.py", "runserver",
                    "0.0.0.0:8000", "--configuration=Dev"]
            execute_from_command_line(args)
    else:
        # Perform ordinary manage.py functionality
        execute_from_command_line(sys.argv)
