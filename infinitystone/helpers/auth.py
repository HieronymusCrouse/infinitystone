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
from luxon import g
from luxon import db
from luxon.utils.password import valid as is_valid_password
from luxon.exceptions import AccessDeniedError
from infinitystone.models.users import infinitystone_user

def localize(username, domain):
    default_role = g.app.config.get(
        'identity', 'default_tenant_role',
        fallback='Customer')

    with db() as conn:
        values = [username, ]
        sql = 'SELECT username FROM infinitystone_user'
        sql += ' WHERE'
        sql += ' username = %s'
        if domain is not None:
            sql += ' AND domain = %s'
            values.append(domain)
        else:
            sql += ' AND domain IS NULL'
        result = conn.execute(sql,
                              values).fetchone()

        if not result:
            user_obj = infinitystone_user()
            user_obj['username'] = username
            if domain:
                user_obj['domain'] = domain

            user_obj.commit()
            user_id = user_obj.id
            

def authorize(username=None, password=None, domain=None):
    with db() as conn:
        values = [username, ]
        sql = 'SELECT username, password FROM infinitystone_user'
        sql += ' WHERE'
        sql += ' username = %s'
        if domain is not None:
            sql += ' AND domain = %s'
            values.append(domain)
        else:
            sql += ' AND domain IS NULL'

        crsr = conn.execute(sql, values)
        result = crsr.fetchone()
        if result is not None:
            # Validate Password againts stored HASHED Value.
            if is_valid_password(password, result['password']):
                return True

        raise AccessDeniedError('Invalid credentials provided')
