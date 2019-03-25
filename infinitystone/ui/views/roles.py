# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 Christiaan Frans Rademan.
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
from luxon import g
from luxon import router
from luxon import register
from luxon import render_template
from luxon.utils.bootstrap4 import form

from infinitystone.ui.models.roles import infinitystone_role

g.nav_menu.add('/System/Roles',
               href='/system/roles',
               tag='infrastructure:admin',
               endpoint='identity',
               feather='shield')


@register.resources()
class Roles():
    def __init__(self):
        router.add('GET',
                   '/system/roles',
                   self.list,
                   tag='roles:view')

        router.add('GET',
                   '/system/roles/{id}',
                   self.view,
                   tag='roles:view')

        router.add('GET',
                   '/system/roles/delete/{id}',
                   self.delete,
                   tag='roles:admin')

        router.add(('GET', 'POST',),
                   '/system/roles/add',
                   self.add,
                   tag='roles:admin')

        router.add(('GET', 'POST',),
                   '/system/roles/edit/{id}',
                   self.edit,
                   tag='roles:admin')

    def list(self, req, resp):
        return render_template('infinitystone.ui/roles/list.html',
                               view='Roles')

    def delete(self, req, resp, id):
        req.context.api.execute('DELETE', '/v1/role/%s' % id,
                                endpoint='identity')

    def view(self, req, resp, id):
        role = req.context.api.execute('GET', '/v1/role/%s' % id,
                                       endpoint='identity')
        html_form = form(infinitystone_role, role.json, readonly=True)
        return render_template('infinitystone.ui/roles/view.html',
                               view='View Role',
                               form=html_form,
                               id=id)

    def edit(self, req, resp, id):
        if req.method == 'POST':
            req.context.api.execute('PUT', '/v1/role/%s' % id,
                                    data=req.form_dict,
                                    endpoint='identity')
            return self.view(req, resp, id)
        else:
            role = req.context.api.execute('GET', '/v1/role/%s' % id,
                                           endpoint='identity')
            html_form = form(infinitystone_role, role.json)
            return render_template('infinitystone.ui/roles/edit.html',
                                   role=role.json['name'],
                                   view='Edit Role',
                                   form=html_form,
                                   id=id)

    def add(self, req, resp):
        if req.method == 'POST':
            response = req.context.api.execute('POST', '/v1/role',
                                               data=req.form_dict,
                                               endpoint='identity')
            return self.view(req, resp, response.json['id'])
        else:
            html_form = form(infinitystone_role)
            return render_template('infinitystone.ui/roles/add.html',
                                   view='Add Role',
                                   form=html_form)
