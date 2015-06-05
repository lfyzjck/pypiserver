#!/usr/bin/env python
# coding: utf-8
import urllib2
import logging

from bottle import HTTPError


logger = logging.getLogger("pypiserver")


def validate_package_name(name, fallback_url):
    if not name == name.lower():
        logger.warning("package name may not contains upper case: %s" % name)
        raise HTTPError(400, output="package name may not contains uppercase")
    if existed_package_name(fallback_url, name):
        logger.warning("package name already exists: %s" % name)
        raise HTTPError(400, output="package already exists")


def validate_package_version(version):
    pass


def existed_package_name(fallback_url, package_name):
    package_url = "{0}/{1}".format(fallback_url, package_name)
    try:
        req = urllib2.Request(url=package_url)
        urllib2.urlopen(req, timeout=2)
    except urllib2.HTTPError as e:
        if e.code == 404:
            return False
    return True
