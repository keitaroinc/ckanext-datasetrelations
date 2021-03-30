"""
ckanext-datasetrelations
Copyright (c) 2017 Keitaro AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# -*- coding: utf-8 -
import logging

import ckan.plugins as p
import ckan.logic as l
import ckan.model as m
import ckan.plugins.toolkit as t
from jinja2.runtime import Undefined

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

log = logging.getLogger(__name__)


def datasetrelations_get_user_available_datasets(user):
    out = []
    datasets = l.get_action('available_datasets_for_user')({'user': user})
    for _ in datasets:
        obj = m.Package.get(_)
        out.append({'name': obj.title, 'value': obj.id})
    return out


def datasetrelations_get_dataset_relations(id, return_obj=False):
    out = []
    if id in (None, '', Undefined):
        return out

    datasets = l.get_action('dataset_relationships_show')({}, {'id': id})
    for _ in datasets:
        obj = m.Package.get(_['subject'])
        if return_obj:
            out.append(obj.as_dict())
        else:
            out.append(obj.id)
    return out


def get_package_relations(id):
    out = []
    if id in (None, '', Undefined):
        return out
    rels = l.get_action('dataset_relationships_show')({}, {'id': id})
    return rels


def extra_package_output(value):
    package = l.get_action('package_show')({'ignore_auth': True}, {'id': value})
    return package['title']
