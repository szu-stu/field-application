#-*- coding: utf-8 -*-
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ''' used by models.FileField '''
    supported_extension = ('txt', 'doc', 'docx')
    for extension in supported_extension:
        if value.name.endswith(extension):
            return
    raise ValidationError(u'不能上传该格式的文件')
