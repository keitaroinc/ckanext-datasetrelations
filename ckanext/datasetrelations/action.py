# -*- coding: utf-8 -
import logging

import ckan.plugins as p
import ckan.logic as l
import ckan.plugins.toolkit as t
import ckanext.datasetrelations.helpers as h

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

log = logging.getLogger(__name__)


def package_update(context, data_dict):
    def _create_package_relationship(subject, object, type=None):
        if type is None:
            type = 'depends_on'
        l.get_action('package_relationship_create')(context, {
            'subject': subject,
            'object': object,
            'type': type
        })

    def _delete_package_relationship(subject, object, type=None):
        if type is None:
            type = 'depends_on'
        l.get_action('package_relationship_delete')(context, {
            'subject': subject,
            'object': object,
            'type': type
        })

    related = data_dict.pop('related-datasets', [])
    if isinstance(related, list):
        pass
    elif isinstance(related, basestring):
        related = [related]

    pkg_id = data_dict['id']
    existing = h.datasetrelations_get_dataset_relations(pkg_id)

    related_set = set(related)
    existing_set = set(existing)

    # Check for difference
    diff = existing_set.difference(related_set)

    # Check for new
    for rel in related:
        if rel in existing:
            continue
        try:
            _create_package_relationship(subject=rel, object=pkg_id)
        except Exception as e:
            log.error(str(e))

    for rel in diff:
        _delete_package_relationship(subject=rel, object=pkg_id)

    return data_dict

@l.side_effect_free
def dataset_relationships_show(context, data_dict):
    # TODO: Add auth function
    m = context['model']
    session = context['session']
    id_or_name = l.get_or_bust(data_dict, 'id')
    pkg_dict = l.action.get.package_show(context, {'id': id_or_name})
    _id = pkg_dict['id']
    rels = session.query(m.PackageRelationship) \
        .filter(m.PackageRelationship.object_package_id == _id,
                m.PackageRelationship.state == 'active').all()
    out = map(lambda rel: rel.as_dict(), rels)
    return out


@l.side_effect_free
def available_datasets_for_user(context, data_dict):
    # TODO: Add auth
    user = context.get('user', None)
    if user is None:
        return []

    out = []
    orgs = l.get_action('organization_list_for_user')(context, {'id': user})
    for o in orgs:
        _ = l.get_action('organization_show')(context, {'id': o['id'], 'include_datasets': True})
        out.extend(map(lambda d: d['name'], _['packages']))

    out = set(out)
    return list(out)
