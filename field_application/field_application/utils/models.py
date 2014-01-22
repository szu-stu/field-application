#-*- coding: utf-8 -*-
import os


def file_save_path(app_name):
    ''' decorator of gennerate_path()
    '''
    def gennerate_path(instance, filename):
        ''' this function indicate the uploaded file saving path
            which is used in models.py,
            passed as parameter in model Field constructor
            invoked by django.
        '''
        return os.path.join(app_name, instance.organization.user.username,
                            instance.activity + '_' + filename)
    return gennerate_path


def get_second_key(first_key, choices):
    ''' get the second key of the choices used in models
        corresponding to the first key '''
    for t in choices:
        if t[0] == first_key:
            return t[1]
    raise Exception("can't find correspoding key in choices for:" \
            + str(first_key))


def get_first_key(second_key, choices):
    ''' get the first key of the choices used in models
        corresponding to the second key '''
    for t in choices:
        if t[1] == second_key:
            return t[0]
    raise Exception("can't find correspoding key in choices for:" \
            + str(second_key))
