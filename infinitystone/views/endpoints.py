# -*- coding: utf-8 -*-
# Copyright (c) 2018-2020 Christiaan Frans Rademan <chris@fwiw.co.za>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
from luxon import register
from luxon import router
from luxon.helpers.api import sql_list, obj
from luxon.utils import sql

from infinitystone.models.endpoints import infinitystone_endpoint


@register.resources()
class Endpoints(object):
    def __init__(self):
        router.add('GET', '/v1/endpoint/{id}', self.endpoint,
                   tag='endpoints:view')
        router.add('GET', '/v1/endpoints', self.endpoints)
        router.add('GET', '/v1/regions', self.regions)
        router.add('POST', '/v1/endpoint', self.create,
                   tag='endpoints:admin')
        router.add(['PUT', 'PATCH'], '/v1/endpoint/{id}', self.update,
                   tag='endpoints:admin')
        router.add('DELETE', '/v1/endpoint/{id}', self.delete,
                   tag='endpoints:admin')

    def endpoint(self, req, resp, id):
        return obj(req, infinitystone_endpoint, sql_id=id)

    def regions(self, req, resp):
        select = sql.Select('infinitystone_endpoint')
        select.group_by = sql.Field('region')

        return sql_list(req, select, fields=('region',))

    def endpoints(self, req, resp):
        return sql_list(req,
                        'infinitystone_endpoint',
                        search={'name': str,
                                'interface': str,
                                'region': str,
                                'uri': str})

    def create(self, req, resp):
        endpoint = obj(req, infinitystone_endpoint)
        endpoint.commit()
        return endpoint

    def update(self, req, resp, id):
        endpoint = obj(req, infinitystone_endpoint, sql_id=id)
        endpoint.commit()
        return endpoint

    def delete(self, req, resp, id):
        endpoint = obj(req, infinitystone_endpoint, sql_id=id)
        endpoint.commit()
        return endpoint
