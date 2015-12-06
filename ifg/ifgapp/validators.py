# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError


def validate_file_ispdf(value):
    return validate_file_extension(value, ['.pdf'], u'O arquivo não é formato PDF')


def validate_file_extension(value, valid_extensions, message=u'Unsupported file extension.'):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    if not ext in valid_extensions:
        raise ValidationError(message)


def validate_telefone(numero):
    if not numero.isdigit():
        return False
    n = str(int(numero.strip()))
    return len(n) in (8, 10)


