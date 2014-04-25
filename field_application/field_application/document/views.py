#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from field_application.document.models import Document
from field_application.document.forms import DocumentForm
from field_application.account.permission import check_perms

def index(request):
    doc_list = Document.objects.all()
    return render(request, 'document/index.html', {'doc_list':doc_list})

class UploadFileView(View):
    @method_decorator(login_required)
    @method_decorator(check_perms('account.manager', u'无管理权限'))
    def post(self, request):
        doc_list = Document.objects.all()
        form = DocumentForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'document/document.html', {'form':form, 'doc_list':doc_list})
        form.save()
        return HttpResponseRedirect(reverse('document:upload'))

    @method_decorator(login_required)
    @method_decorator(check_perms('account.manager', u'无管理权限'))
    def get(self, request):
        form = DocumentForm()
        doc_list = Document.objects.all()
        return render(request, 'document/document.html', {'form':form, 'doc_list':doc_list})

@check_perms('account.manager', u'无管理权限')
def delete(request):
    doc_id = request.GET.get('id')
    doc = get_object_or_404(Document, id=doc_id)
    doc.delete()
    return HttpResponseRedirect(reverse('document:upload'))
