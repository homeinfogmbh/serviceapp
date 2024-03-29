#! /usr/bin/env python3
"""Install script."""

from setuptools import setup


setup(
    name="serviceapp",
    use_scm_version={"local_scheme": "node-and-timestamp"},
    setup_requires=["setuptools_scm"],
    install_requires=[
        "authlib",
        "basex",
        "configlib",
        "mdb",
        "oauth2gen",
        "peewee",
        "peeweeplus",
        "flask",
        "werkzeug",
        "wsgilib",
    ],
    author="HOMEINFO - Digitale Informationssysteme GmbH",
    author_email="<info@homeinfo.de>",
    maintainer="Richard Neumann",
    maintainer_email="<r.neumann@homeinfo.de>",
    packages=["tenant2tenant"],
    license="GPLv3",
    description="Web application backend for service contractors.",
)
