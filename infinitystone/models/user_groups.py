# -*- coding: utf-8 -*-
# Copyright (c) 2018 Christiaan Frans Rademan.
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
from infinitystone.models.groups import infinitystone_group


@register.model()
class infinitystone_user_group(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    group_id = SQLModel.Uuid()
    domain = SQLModel.Fqdn(internal=True)
    tenant_id = SQLModel.String()
    user_id = SQLModel.Uuid()
    creation_time = SQLModel.DateTime(readonly=True, default=now)
    unique_user_group = SQLModel.UniqueIndex(group_id, user_id)
    user_group_id_ref = SQLModel.ForeignKey(group_id, infinitystone_group.id)
    user_group_domain_ref = SQLModel.ForeignKey(domain, infinitystone_domain.name)
    user_group_tenant_ref = SQLModel.ForeignKey(tenant_id, infinitystone_tenant.id)
    group_index = SQLModel.Index(group_id)
    domain_group_index = SQLModel.Index(domain, group_id)
    tenant_group_index = SQLModel.Index(tenant_id, group_id)
    tenant_domain_group_index = SQLModel.Index(domain, tenant_id, group_id)
    primary_key = id