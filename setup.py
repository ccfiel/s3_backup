# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='s3_backup',
    version=version,
    description='Use Amazon S3 Backup for Frappe and ERPNext',
    author='Chris Ian Fiel',
    author_email='ccfiel@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
