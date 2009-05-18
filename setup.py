#!/usr/bin/env python

from distutils.core import setup

setup(name='django-routines',
    version='0.1',
    description='Common Django tags and shortcuts',
    author='Andrii Kurinnyi',
    author_email='andrew@zen4ever.com',
    url='http://github.com/zen4ever/django-routines/tree/master',
    packages=['routines', 'routines.templatetags'],
    )

