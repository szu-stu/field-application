#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404

from models import Document
from forms import DocumentForm

from field_application.account.permission import check_perms

def index(request):
    form=DocumentForm()
    doc_list=Document.objects.all()
    return render(request,'document/index.html',{'form':form,'doc_list':doc_list})

@check_perms('account.manager', u'无管理权限')
def Upload_File(request):
    form=DocumentForm()
    doc_list=Document.objects.all()

    if request.method=='POST':
        form=DocumentForm(request.POST,request.FILES)
        if not form.is_valid():
            return render(request,'document/document.html',{'form':form, 'doc_list':doc_list})
        form.save()
        return HttpResponseRedirect('/document/modify')

    else:
        return render(request,'document/document.html',{'form':form,'doc_list':doc_list})

@check_perms('account.manager', u'无管理权限')
def del_doc(request):
    doc_id=request.GET.get('id')
    doc=get_object_or_404(Document, id=doc_id)
    doc.delete()
    return HttpResponseRedirect('/document/modify')
