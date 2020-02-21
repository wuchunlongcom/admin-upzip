# -*- coding: UTF-8 -*-
import os
import sys
import django
import random

print('python 版本: %s。\ndjango版本: %s。'%(sys.version, django.get_version()))



if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()
    from django.contrib.auth.models import User, Group, Permission


    
    #组添加权限 django==2.2.6 通用
    operatorGroup = Group.objects.create(name='Operator')
    operatorGroup.permissions.add(
        #Permission.objects.get(name='Can add blog'),
              
    )
    operatorGroup.save()
    
    customerGroup = Group.objects.create(name='Customer')
    customerGroup.permissions.add()
    customerGroup.save()
        
    if not User.objects.filter(username = 'admin'):
        User.objects.create_superuser('admin', 'admin@test.com','admin')     


