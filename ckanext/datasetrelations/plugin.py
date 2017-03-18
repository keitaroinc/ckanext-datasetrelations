# -*- coding: utf-8 -
import logging

import ckan.plugins as p
import ckan.plugins.toolkit as t
import ckanext.datasetrelations.action as a
import ckanext.datasetrelations.helpers as h

try:
    # CKAN 2.7 and later
    from ckan.common import config
except ImportError:
    # CKAN 2.6 and earlier
    from pylons import config

log = logging.getLogger(__name__)


class DatasetrelationsPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.IActions)
    p.implements(p.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        t.add_template_directory(config_, 'templates')
        t.add_public_directory(config_, 'public')
        t.add_resource('fanstatic', 'datasetrelations')

    # IActions
    def get_actions(self):
        return {
            'available_datasets_for_user': a.available_datasets_for_user,
            'dataset_relationships_show': a.dataset_relationships_show,
            'datasetrelations_package_update': a.package_update,
        }

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_user_available_datasets': h.datasetrelations_get_user_available_datasets,
            'get_dataset_relations': h.datasetrelations_get_dataset_relations,
            'get_package_relations': h.get_package_relations,
            'extra_package_output': h.extra_package_output
        }
