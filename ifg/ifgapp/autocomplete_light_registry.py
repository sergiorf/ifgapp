# -*- coding: utf-8 -*-
import autocomplete_light.shortcuts as al
from models import Inventor
import autocomplete_light


class InventorAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['username']
    attrs = {
        'placeholder': 'Nome do usuário',
        'data-autocomplete-minimum-characters': 0,
    }
    widget_attrs = {'data-widget-maximum-values': 4}
    model = Inventor

autocomplete_light.register(Inventor, InventorAutocomplete)

