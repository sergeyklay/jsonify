# This file is part of the Jsonify.
#
# Copyright (c) 2021 airSlate, Inc.
#
# For the full copyright and license information, please view
# the LICENSE file that was distributed with this source code

from asdicts.dict import path


# TODO: Do I need a class fro this?
class SettingsTransformer:

    CHOICE = 'choice'
    RADIO_GROUP_MANUAL = 'radio_group_manual'
    MULTIPLE_CHOICE = 'multiple_choice'
    SEQUENCE = 'sequence'
    FIELDS_MAPPING = 'fields_mapping'
    MATCH = 'match'
    MAPPING = 'mapping'
    GROUP = 'group'

    def transform(self, settings=None) -> dict:
        if settings is None:
            settings = dict()
        elif isinstance(settings, dict):
            return settings

        # TODO: Raise exception on non list data type
        return self.from_list(settings)

    def from_list(self, settings: list) -> dict:
        result = dict()
        for s in settings:
            # TODO: Raise exception on non dict data type
            result[s['name']] = self._transform_setting(s)
        return result

    def _transform_setting(self, setting: dict):
        setting_type = str(setting.get('type', ''))

        # TODO: radio_group_manual, multiple_choice, sequence
        # TODO: fields_mapping, match, mapping, group
        if setting_type in [self.CHOICE, self.RADIO_GROUP_MANUAL]:
            return path(setting, 'data.value')
        else:
            return None
