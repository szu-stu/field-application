#-*- coding: utf-8 -*-
import logging
import datetime

from django.views.generic import View
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.forms import NON_FIELD_ERRORS
from django.core.paginator import InvalidPage, Paginator

from field_application.campus_field.forms import ExhibitApplicationForm
from field_application.campus_field.models import ExhibitApplication
from field_application.utils.ajax import render_json
from field_application.account.permission import check_perms, check_ownership
from field_application.account.permission import check_not_approved
from field_application.campus_field.forms import check_exhibit_board_num
from field_application.utils.forms import SearchForm
from field_application.utils.views import search_application 


class ApplyView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'campus_field/exhibit/form.html', 
                      {'form': ExhibitApplicationForm(),
                       'post_url': reverse('exhibit:apply')})

    @method_decorator(login_required)
    def post(self, request):
        form = ExhibitApplicationForm(request.POST,
                                      request.FILES)
        if not form.is_valid():
            return render(request, 'campus_field/exhibit/form.html', 
                          {'form': form,
                           'post_url': reverse('exhibit:apply')})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('exhibit:manage'))


def display_table(request):
    week = int(request.GET.get('week') or 0)
    table = ExhibitApplication.generate_table(offset=week)
    return render(request, 'campus_field/exhibit/table.html',
            {'table': table, 'curr_week': week})


def generate_page(listing, request):
    for app in listing:
        app.date = app.start_date.strftime('%Y年%m月%d日') \
            + '-' + app.end_date.strftime('%Y年%m月%d日')
    paginator = Paginator(listing, 40)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return page


class ListAppView(View):

    def get(self, request):
        listing = ExhibitApplication.objects.all().order_by('-pk')
        return render(request, 'list.html',
                    {'page': generate_page(listing, request),
                     'title': u'校园展览场地申请',
                     'form': SearchForm()})

    def post(self, request):
        form = SearchForm(request.POST)
        if not form.is_valid():
            listing = \
                ExhibitApplication.objects.all().order_by('-pk')
        else:
            listing = search_application(ExhibitApplication,
                                         form).order_by('-pk')
        return render(request, 'list.html',
                    {'page': generate_page(listing, request),
                     'title': u'校园展览场地申请',
                     'form': form})


class ManageView(View):

    @method_decorator(login_required)
    def get(self, request):
        return ManageView.manage(request,
            ExhibitApplication.objects.all(),
            SearchForm())

    @method_decorator(login_required)
    def post(self, request):
        form = SearchForm(request.POST)
        if not form.is_valid():
            listing = \
                ExhibitApplication.objects.all().order_by('-pk')
        else:
            listing = search_application(ExhibitApplication,
                                         form)
        return ManageView.manage(request, listing, form)

    @classmethod
    def manage(cls, request, listing, form):
        org = request.user.organization
        if org.user.has_perm('account.manager'):
            listing = listing.order_by('-pk')
        else:
            listing = listing.filter(organization=org).order_by('-pk')
        page = generate_page(listing, request)
        return render(request, 'manage.html',
                {'page': page, 'title': u'校园展览场地申请',
                 'modify_url': reverse('exhibit:modify'),
                 'approve_url': reverse('exhibit:manager_approve'),
                 'delete_url': reverse('exhibit:delete'),
                 'form': form})

 
def get_detail(request):
    app_id = request.GET.get('id')
    app = get_object_or_404(ExhibitApplication, id=app_id)
    data = {'organization': app.organization.chinese_name,
            'place': app.place, 
            'start_date': app.start_date.strftime('%Y年%m月%d日'),
            'end_date': app.end_date.strftime('%Y年%m月%d日'),
            'time': app.time,
            'activity': app.activity,
            'approved': app.approved, 'plan_file': app.plan_file.url,
            'applicant_name': app.applicant_name,
            'applicant_phone_number': app.applicant_phone_number,
            'applicant_stu_id': app.applicant_stu_id,
            'applicant_college': app.applicant_college,
            'application_time': \
                    app.application_time.strftime('%Y年%m月%d日 %H:%M:%S'),
            'sponsor': app.sponsor, 'sponsorship': app.sponsorship,
            'sponsorship_usage': app.sponsorship_usage,
            'activity_summary': app.activity_summary,
            'exhibit_board_number': app.exhibit_board_number,
            'exhibition': app.exhibition,
            'remarks': app.remarks,
            'id': app_id,
            'user_is_manager': request.user.has_perm('account.manager')}
    return render_json(data)


class ModifyView(View):

    @method_decorator(login_required)
    @method_decorator(check_ownership(ExhibitApplication))
    @method_decorator(check_not_approved(ExhibitApplication))
    def get(self, request):
        app_id = request.GET.get('id')
        app = get_object_or_404(ExhibitApplication, id=app_id)
        form = ExhibitApplicationForm(instance=app)
        return render(request, 'campus_field/exhibit/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': \
                     reverse('exhibit:modify')+'?id='+app_id})

    @method_decorator(login_required)
    @method_decorator(check_ownership(ExhibitApplication))
    @method_decorator(check_not_approved(ExhibitApplication))
    def post(self, request):
        app_id = request.GET.get('id')
        app = get_object_or_404(ExhibitApplication, id=app_id)
        form = ExhibitApplicationForm(
                request.POST, request.FILES, instance=app)
        if not form.is_valid():
            return render(request, 'campus_field/exhibit/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': \
                     reverse('exhibit:modify')+'?id='+app_id})
        form.save()
        return HttpResponseRedirect(reverse('exhibit:manage'))


@login_required
@check_ownership(ExhibitApplication)
@check_not_approved(ExhibitApplication)
def delete(request):
    app_id = request.GET.get('id')
    app = get_object_or_404(ExhibitApplication, id=app_id)
    app.delete()
    return HttpResponseRedirect(reverse('exhibit:manage'))

@login_required
@check_perms('account.manager', u'无管理权限')
def manager_approve(request):
    app_id = request.GET.get('id')
    app = get_object_or_404(ExhibitApplication, id=app_id)
    today = datetime.date.today()
    if not app.approved and (app.start_date < today or app.end_date < today):
        return render(request, 'deny.html',
                {'message': u'所申请的使用时间已过'})
    app.approved = not app.approved
    app.save()
    return HttpResponseRedirect(reverse('exhibit:manage'))

