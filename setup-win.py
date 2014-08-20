#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga

import os
import sys
import py2exe

sys.path.append(os.path.abspath('../'))

from distutils.core import setup

from configuration import Config

try:
    target = os.environ['PY2EXE_MODE']
except KeyError:
    target = 'multi'

if target == 'single':
    ZIPFILE = None
    BUNDLES = 1
else:
    ZIPFILE = 'shared.lib'
    BUNDLES = 1

setup(windows=[{'script': Config.NAME_MAIN, \
                'icon_resources': [(0, Config.APP_LOGO_ICO)]}],
      options={'py2exe': {
                    'includes': ['sip'],
                    'compressed': True,
                    'bundle_files': BUNDLES,
                    },
               },
      zipfile=ZIPFILE,
)
