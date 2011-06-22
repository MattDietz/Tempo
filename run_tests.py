#!/usr/bin/env python

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import os
import sys

import nose
import nose.config
import nose.core

possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]),
                                   os.pardir,
                                   os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'tempo', '__init__.py')):
    sys.path.insert(0, possible_topdir)

if __name__ == '__main__':
    test_path = os.path.abspath(os.path.join('tests'))
    c = nose.config.Config(stream=sys.stdout,
                      env=os.environ,
                      verbosity=3,
                      workingDir=test_path)
    nose.core.run(config=c, argv=sys.argv)
