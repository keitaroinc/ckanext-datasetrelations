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
