# -*- coding: utf-8 -*-
from models import Inventor, Instituicao
import autocomplete_light


class InventorAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['username']
    attrs = {
        'placeholder': 'Nome do usuário',
        'data-autocomplete-minimum-characters': 0,
    }
    limit_choices = 10
    model = Inventor


class InstituicaoAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['nome', 'sigla']
    attrs = {
        'placeholder': 'Nome ou sigla da instituição',
        'data-autocomplete-minimum-characters': 0,
    }
    limit_choices = 10
    model = Instituicao

autocomplete_light.register(Inventor, InventorAutocomplete)
autocomplete_light.register(Instituicao, InstituicaoAutocomplete)

