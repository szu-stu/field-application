# field-application
### 学子天地场地申请管理系统
-----
下载源代码
```
git clone https://github.com/szu-stu/field-application
```

安装依赖环境
```
pip install -r requirements.txt
```

如果是用virtualenv运行，需要修改settings.py
```
STATICFILES_DIRS = (
    path('field_application', 'static'),
    path('../../django/contrib/admin/static') # 此处为virtualenv中Django目录下admin文件夹
)
    
TEMPLATE_DIRS = (
    path('field_application', 'templates'),
    path('../../django/contrib/admin/templates')
)
```

开启服务器运行即可
