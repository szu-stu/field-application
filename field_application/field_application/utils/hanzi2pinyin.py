# -*- coding:utf-8 -*-
from field_application.settings import path
from field_application.utils.pinyin import PinYin


trans = PinYin(dict_file=path('field_application', 'utils', 'word.data'))
trans.load_word()
