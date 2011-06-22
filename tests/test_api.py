# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

import json
import unittest

import stubout

from tempo import api
from tempo import db

class APITest(unittest.TestCase):
    def setUp(self):
        self.app = api.app.test_client()
        self.stubs = stubout.StubOutForTesting()

    def tearDown(self):
        self.stubs.UnsetAll()

    def test_bad_route(self):
        res = self.app.get('/foo')
        self.assertEqual(res.status_code, 404)

    def test_index_no_items(self):
        res = self.app.get('/%s' % api.resources_name)
        body = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(body[api.resources_name]), 0)

    def test_index_with_items(self):
        def stubbed_index():
            elements = [1,2,3,4,5]
            return elements

        self.stubs.Set(db, 'task_get_all', stubbed_index)
        res = self.app.get('/%s' % api.resources_name)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertEqual(len(body[api.resources_name]), 5)

    def test_show_item(self):
        def stubbed_show(id):
            return 'foo'

        self.stubs.Set(db, 'task_get', stubbed_show)
        res = self.app.get('/%s/1' % api.resources_name)
        self.assertEqual(res.status_code, 200)
        body = json.loads(res.data)
        self.assertEqual(body[api.resource_name], 'foo')

    def test_create_item(self):
        self.called = False
        def stubbed_create(id, values):
            self.called = True
            return values

        self.stubs.Set(db, 'task_create_or_update', stubbed_create)
        res = self.app.post('/%s/1' % api.resources_name)
        self.assertEqual(res.status_code, 202)

    def test_create_item(self):
        self.called = False
        def stubbed_create(id, values):
            self.called = True
            return values

        self.stubs.Set(db, 'task_create_or_update', stubbed_create)
        body = {'task': 'backup', 'instance_uuid': 'abcdef',
                'recurrence': '0 0 0 0 0' }
        res = self.app.post('/%s/1' % api.resources_name,
                            content_type='application/json',
                            data=json.dumps(body))
        self.assertEqual(self.called, True)
        self.assertEqual(res.status_code, 202)

    def test_create_item_with_put(self):
        self.called = False
        def stubbed_create(id, values):
            self.called = True
            return values

        self.stubs.Set(db, 'task_create_or_update', stubbed_create)
        body = {'task': 'backup', 'instance_uuid': 'abcdef',
                'recurrence': '0 0 0 0 0' }
        res = self.app.put('/%s/1' % api.resources_name,
                            content_type='application/json',
                            data=json.dumps(body))
        self.assertEqual(self.called, True)
        self.assertEqual(res.status_code, 202)

    def test_create_item_no_task_fails(self):
        self.called = False
        def stubbed_create(id, values):
            self.called = True
            return values

        self.stubs.Set(db, 'task_create_or_update', stubbed_create)
        body = {'instance_uuid': 'abcdef', 'recurrence': '0 0 0 0 0'}
        res = self.app.put('/%s/1' % api.resources_name,
                            content_type='application/json',
                            data=json.dumps(body))
        self.assertEqual(self.called, False)
        self.assertEqual(res.status_code, 412)

    def test_create_item_no_uuid_fails(self):
        self.called = False
        def stubbed_create(id, values):
            self.called = True
            return values

        self.stubs.Set(db, 'task_create_or_update', stubbed_create)
        body = {'task': 'backup', 'recurrence': '0 0 0 0 0' }
        res = self.app.put('/%s/1' % api.resources_name,
                            content_type='application/json',
                            data=json.dumps(body))
        self.assertEqual(self.called, False)
        self.assertEqual(res.status_code, 412)

    def test_create_item_no_recurrence_fails(self):
        self.called = False
        def stubbed_create(id, values):
            self.called = True
            return values

        self.stubs.Set(db, 'task_create_or_update', stubbed_create)
        body = {'task': 'backup', 'instance_uuid': 'abcdef'}
        res = self.app.put('/%s/1' % api.resources_name,
                            content_type='application/json',
                            data=json.dumps(body))
        self.assertEqual(self.called, False)
        self.assertEqual(res.status_code, 412)
