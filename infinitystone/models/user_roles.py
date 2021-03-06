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
from infinitystone.models.roles import infinitystone_role

USER_ROLES = [
    ('00000000-0000-0000-0000-000000000000',
     '00000000-0000-0000-0000-000000000000',
     None,
     None,
     '00000000-0000-0000-0000-000000000000',
     now()),
]


@register.model()
class infinitystone_user_role(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    role_id = SQLModel.Uuid()
    domain = SQLModel.Fqdn(internal=True)
    tenant_id = SQLModel.String()
    user_id = SQLModel.Uuid()
    user_role_index = SQLModel.Index(user_id, domain, tenant_id)
    creation_time = SQLModel.DateTime(readonly=True, default=now)
    unique_tenant_role = SQLModel.UniqueIndex(domain, role_id, tenant_id, user_id)
    user_id_index = SQLModel.Index(user_id, domain, tenant_id)
    user_role_id_ref = SQLModel.ForeignKey(role_id, infinitystone_role.id,
                                           on_delete='RESTRICT')
    user_role_domain_ref = SQLModel.ForeignKey(domain,
                                               infinitystone_domain.name,
                                               on_delete='RESTRICT',
                                               on_update='RESTRICT')
    user_role_tenant_ref = SQLModel.ForeignKey(tenant_id,
                                               infinitystone_tenant.id)
    primary_key = id
    db_default_rows = USER_ROLES
