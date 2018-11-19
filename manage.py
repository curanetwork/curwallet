#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(verbose=True)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "curwallet.settings.development")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
