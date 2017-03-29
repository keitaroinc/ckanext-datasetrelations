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
