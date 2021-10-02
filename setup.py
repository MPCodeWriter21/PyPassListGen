#!/usr/bin/env python3
# setup.py
# CodeWriter21

from setuptools import setup, Extension, find_packages
from distutils.command.build import build


class Build(build):
    def finalize_options(self):
        super().finalize_options()
        from Cython.Build import cythonize
        self.distribution.ext_modules = cythonize(self.distribution.ext_modules)


with open('README.md', 'r') as file:
    long_description = file.read()

with open('LICENSE.txt', 'r') as file:
    LICENSE = file.read()

DESCRIPTION = 'PyPassListGen is a python script that allows you to generate password lists fast and easily.'
VERSION = '1.0.1'
EXT_MODULES = [Extension(name='PPLG.lib.Generate_cy', sources=["PPLG/lib/Generate_cy.pyx"])]

setup(
    name='PyPassListGen',
    version=VERSION,
    url='https://github.com/MPCodeWriter21/PyPassListGen',
    author='CodeWriter21(Mehrad Pooryoussof)',
    author_email='<CodeWriter21@gmail.com>',
    license=LICENSE,
    description=DESCRIPTION,
    long_description='See https://github.com/MPCodeWriter21/PyPassListGen',
    long_description_content_type='text/plain',
    install_requires=['log21', 'importlib_resources'],
    setup_requires=['cython'],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['PyPassListGen = PPLG:entry_point', 'PPLG = PPLG:entry_point']
    },
    ext_modules=EXT_MODULES,
    keywords=['python', 'pass', 'password', 'passlist', 'passwordlist', 'password-list', 'password list generator',
              'PyPassListGen', 'CodeWriter21'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
    cmdclass={"build": Build},
    include_package_data=True
)
