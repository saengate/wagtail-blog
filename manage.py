#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json


def main():
    environments = {
        'local': 'local',
        'production': 'production',
    }
    environment = os.getenv('ENV', 'local')

    settings = os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE', 'config.settings.' + environment)
    env = environments[environment]
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

    print(env)
    with open('zappa_settings.json') as environment:
        data = json.load(environment)
        env_vars = data[env]['environment_variables']
    for item in env_vars:
        os.environ.setdefault(item, env_vars[item])

    try:
        from django.core.management import execute_from_command_line  # NOQA
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"  # NOQA
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
