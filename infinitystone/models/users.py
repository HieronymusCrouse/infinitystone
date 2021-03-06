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
from uuid import uuid4

from luxon import register
from luxon import SQLModel
from luxon.utils.timezone import now

from infinitystone.models.domains import infinitystone_domain
from infinitystone.models.tenants import infinitystone_tenant

USERS = [
    ('00000000-0000-0000-0000-000000000000',
     None, None,
     'root', '$2b$12$QaWa.Q3gZuafYXkPo3EJRuSJ1wGuutShb73RuH1gdUVri82CU6V5q',
     None, 'Default Root User', None, None, None, None, None, None, 0,
     1, None, now(),),
]


@register.model()
class infinitystone_user(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    domain = SQLModel.Fqdn(internal=True)
    tenant_id = SQLModel.Uuid(internal=True)
    username = SQLModel.Username(max_length=64, null=False)
    password = SQLModel.Password(max_length=150, null=True)
    email = SQLModel.Email(max_length=100)
    name = SQLModel.String(max_length=64)
    phone_mobile = SQLModel.Phone()
    phone_office = SQLModel.Phone()
    designation = SQLModel.Enum('', 'Mr', 'Mrs', 'Ms', 'Dr', 'Prof')
    last_login = SQLModel.DateTime(readonly=True)
    region = SQLModel.String(null=True)
    confederation = SQLModel.String(null=True)
    roaming = SQLModel.Boolean(default=False)
    enabled = SQLModel.Boolean(default=True)
    metadata = SQLModel.MediumText()
    creation_time = SQLModel.DateTime(default=now, readonly=True)
    unique_username = SQLModel.UniqueIndex(username)
    user_tenant_ref = SQLModel.ForeignKey(tenant_id, infinitystone_tenant.id,
                                          on_delete='RESTRICT')
    user_domain_ref = SQLModel.ForeignKey(domain, infinitystone_domain.name,
                                          on_delete='RESTRICT',
                                          on_update='RESTRICT')
    primary_key = id
    db_default_rows = USERS
