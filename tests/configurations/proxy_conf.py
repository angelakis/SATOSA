#!/usr/bin/env python
# pylint: disable = missing-docstring
# -*- coding: utf-8 -*-
import os
from future.backports.test.support import import_module

from saml2 import BINDING_HTTP_REDIRECT
from saml2 import BINDING_HTTP_POST

from example.test_module import TestModule

BASE = 'https://example.com'


def full_path(path):
    return os.path.join(os.path.dirname(__file__), path)


xmlsec_path = '/usr/local/bin/xmlsec1'

ATTRIBUTE_MODULE = TestModule(full_path("../users.json"),
                              "eduPersonPrincipalName")

CONFIG = {
    "backends": {},
    "entityid": "{}/proxy.xml".format(BASE),
    "service": {
        "idp": {
            "endpoints": {
                "single_sign_on_service": [],
            },
        },
    },
    "key_file": full_path("../pki/key.pem"),
    "cert_file": full_path("../pki/cert.pem"),
    "metadata": {
        "local": [full_path("unittest_sp.xml")],
    },
    "xmlsec_binary": xmlsec_path,
}


def add_module(config_path):
    mod_conf = import_module(config_path)
    CONFIG["backends"].update(mod_conf.CONFIG)
    CONFIG["service"]["idp"]["endpoints"]["single_sign_on_service"].append(
        ("%s/%s/sso/redirect" % (BASE, mod_conf.PROVIDER), BINDING_HTTP_REDIRECT))
    CONFIG["service"]["idp"]["endpoints"]["single_sign_on_service"].append(
        ("%s/%s/sso/post" % (BASE, mod_conf.PROVIDER), BINDING_HTTP_POST))


add_module("configurations.saml2_module_conf")
