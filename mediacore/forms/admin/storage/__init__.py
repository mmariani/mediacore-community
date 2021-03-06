# This file is a part of MediaCore CE, Copyright 2009-2012 MediaCore Inc.
# The source code contained in this file is licensed under the GPL.
# See LICENSE.txt in the main project directory, for more information.

from pylons import request
from tw.forms import PasswordField, SingleSelectField
from tw.forms.fields import ContainerMixin as _ContainerMixin
from tw.forms.validators import All, FancyValidator, FieldsMatch, Invalid, NotEmpty, PlainText, Schema

from mediacore.forms import ListFieldSet, ListForm, SubmitButton, TextField
from mediacore.lib.i18n import N_
from mediacore.plugin import events
from mediacore.plugin.abc import abstractmethod

class StorageForm(ListForm):
    template = 'admin/box-form.html'
    id = 'storage-form'
    css_class = 'form storageform'
    submit_text = None
    show_children_errors = True
    _name = 'storage-form' # TODO: Figure out why this is required??
    params = ['engine']

    fields = [
        ListFieldSet('general',
            legend=N_('General Options:'),
            suppress_label=True,
            children=[
                TextField('display_name',
                    label_text=N_('Display Name'),
                    validator=TextField.validator(not_empty=True),
                    maxlength=100,
                ),
            ],
        ),
    ]

    buttons = [
        SubmitButton('save',
            default=N_('Save'),
            css_classes=['btn', 'btn-save', 'blue', 'f-rgt'],
        ),
    ]

    def display(self, value, engine, **kwargs):
        """Display the form with default values from the given StorageEngine.

        If the value dict is not fully populated, populate any missing entries
        with the values from the given StorageEngine's
        :attr:`_data <mediacore.lib.storage.StorageEngine._data>` dict.

        :param value: A (sparse) dict of values to populate the form with.
        :type value: dict
        :param engine: An instance of the storage engine implementation.
        :type engine: :class:`mediacore.lib.storage.StorageEngine` subclass

        """
        general = value.setdefault('general', {})
        if not general.get('display_name', None):
            general['display_name'] = engine.display_name
        return ListForm.display(self, value, engine=engine, **kwargs)

    def save_engine_params(self, engine, general, **kwargs):
        """Map validated field values to engine data.

        Since form widgets may be nested or named differently than the keys
        in the :attr:`mediacore.lib.storage.StorageEngine._data` dict, it is
        necessary to manually map field values to the data dictionary.

        :type engine: :class:`mediacore.lib.storage.StorageEngine` subclass
        :param engine: An instance of the storage engine implementation.
        :param \*\*kwargs: Validated and filtered form values.
        :raises formencode.Invalid: If some post-validation error is detected
            in the user input. This will trigger the same error handling
            behaviour as with the @validate decorator.

        """
        engine.display_name = general['display_name']
