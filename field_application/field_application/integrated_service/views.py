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
from django.utils import timezone

from field_application.account.permission import check_perms, check_ownership
from field_application.integrated_service.forms import InteServiceApplicationForm
from field_application.integrated_service.models import InteServiceApplication
from field_application.utils.ajax import render_json
from field_application.account.permission import check_perms
from field_application.account.permission import check_not_approved
from field_application.utils.forms import SearchForm
from field_application.utils.views import search_application 


def find_conflict_app(id, place, date, time):
    ''' time 的元素为InteServiceApplication.TIME中的时间段
        用","隔开
    '''
    conflict_app = set()
    for t in time.split(','):
        time_like = '%' + t + '%'
        conflict = InteServiceApplication.objects.filter(
                place=place,
                date=date,
                time__like=time_like).exclude(pk=id)
        conflict_app = conflict_app | set(conflict)
    return [{'org': a.organization.chinese_name,
             'topic': a.topic,
             'apply_time': \
                     timezone.localtime(
                         a.application_time).strftime('%Y年%m月%d日 %H:%M:%S'),
             'approved': a.approved,
             'conflict_time': list(set(a.time) & set(time.split(','))),
             'app_id': a.pk} for a in conflict_app]


def conflict_for_form(request):
    ''' return conflict application to form '''
    if request.method != 'GET':
        raise Exception('request method is not GET')
    id = request.GET.get('id')
    time = request.GET.get('time')
    place = request.GET.get('place')
    app_date = datetime.datetime.strptime(request.GET.get('date'),
                                          '%Y-%m-%d').date()
    return render_json(find_conflict_app(id, place, app_date, time))


class ApplyMeetingRoomView(View):

    @method_decorator(login_required)
    @method_decorator(check_perms('account.youth_league_committee',
                                  '非团委下属组织不能申请'))
    def get(self, request):
        return render(request, 'integrated_service/form.html', 
                      {'form': InteServiceApplicationForm(),
                       'post_url': reverse('integrated_service:apply')})

    @method_decorator(login_required)
    @method_decorator(check_perms('account.youth_league_committee',
                                  '非团委下属组织不能申请'))
    def post(self, request):
        form = InteServiceApplicationForm(request.POST)
        if not form.is_valid():
            return render(request, 'integrated_service/form.html', 
                          {'form': form,
                           'post_url': reverse('integrated_service:apply')})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('integrated_service:manage'))


def display_table(request):
    try:
        week = int(request.GET.get('week') or 0)
    except ValueError:
        week = 0
    table = InteServiceApplication.generate_table(offset=week)
    return render(request, 'integrated_service/table.html',
            {'table': table, 'curr_week': week})


def generate_page(listing, request):
    for app in listing:
        app.date = app.date.strftime('%Y年%m月%d日')
        app.activity = app.topic
    paginator = Paginator(listing, 40)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return page

    
class ListAppView(View):

    def get(self, request):
        listing = InteServiceApplication.objects.all().order_by('-pk')
        return render(request, 'list.html',
                    {'page': generate_page(listing, request),
                     'title': u'西南综合服务楼场地申请',
                     'form': SearchForm()})

    def post(self, request):
        form = SearchForm(request.POST)
        if not form.is_valid():
            listing = InteServiceApplication.objects.all().order_by('-pk')
        else:
            listing = search_application(InteServiceApplication,
                                         form).order_by('-pk')
        return render(request, 'list.html',
                    {'page': generate_page(listing, request),
                     'title': u'西南综合服务楼场地申请',
                     'form': form})


class ManageView(View):

    @method_decorator(login_required)
    def get(self, request):
        return ManageView.manage(request,
            InteServiceApplication.objects.all(),
            SearchForm())

    @method_decorator(login_required)
    def post(self, request):
        form = SearchForm(request.POST)
        if not form.is_valid():
            listing = \
                InteServiceApplication.objects.all().order_by('-pk')
        else:
            listing = search_application(InteServiceApplication,
                                         form)
        return ManageView.manage(request, listing, form)

    @classmethod
    def manage(cls, request, listing, form):
        org = request.user.organization
        if org.user.has_perm('account.manager'):
            filtered_list = listing.order_by('-pk')
        else:
            filtered_list = listing.filter(organization=org).order_by('-pk')
        page = generate_page(filtered_list, request)
        return render(request, 'manage.html',
                {'page': page, 'title': u'西南综合服务楼场地申请',
                 'modify_url': reverse('integrated_service:modify'),
                 'approve_url': reverse('integrated_service:manager_approve'),
                 'delete_url': reverse('integrated_service:delete'),
                 'form': form})

 
def get_detail(request):
    app_id=request.GET.get('id')
    app = get_object_or_404(InteServiceApplication, id=app_id)
    data = {'organization': app.organization.chinese_name,
            'place': app.place,
            'date': app.date.strftime('%Y年%m月%d日'),
            'time': app.time,
            'topic': app.topic,
            'approved': app.approved,
            'applicant_name': app.applicant_name,
            'applicant_phone_number': app.applicant_phone_number,
            'applicant_stu_id': app.applicant_stu_id,
            'applicant_college': app.applicant_college,
            'sponsor': app.sponsor, 'sponsorship': app.sponsorship,
            'sponsorship_usage': app.sponsorship_usage,
            'summary': app.summary,
            'remarks': app.remarks,
            'id': app_id,
            'user_is_manager': request.user.has_perm('account.manager'),
            'conflict_apps': \
                    find_conflict_app(app_id, app.place, app.date, ','.join(app.time))}
    return render_json(data)



class ModifyView(View):

    @method_decorator(login_required)
    @method_decorator(check_ownership(InteServiceApplication))
    @method_decorator(check_not_approved(InteServiceApplication))
    def get(self, request):
        app_id = request.GET.get('id')
        app = get_object_or_404(InteServiceApplication, id=app_id)
        form = InteServiceApplicationForm(instance=app)
        return render(request, 'integrated_service/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': reverse('integrated_service:modify')+'?id='+app_id})

    @method_decorator(login_required)
    @method_decorator(check_ownership(InteServiceApplication))
    @method_decorator(check_not_approved(InteServiceApplication))
    def post(self, request):
        app_id = request.GET.get('id')
        app = get_object_or_404(InteServiceApplication, id=app_id)
        form = InteServiceApplicationForm(request.POST, instance=app)
        if not form.is_valid():
            return render(request, 'integrated_service/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': reverse('integrated_service:modify')+'?id='+app_id})
        form.save()
        return HttpResponseRedirect(reverse('integrated_service:manage'))


@login_required
@check_ownership(InteServiceApplication)
@check_not_approved(InteServiceApplication)
def delete(request):
    app_id = request.GET.get('id')
    app = get_object_or_404(InteServiceApplication, id=app_id)
    app.delete()
    return HttpResponseRedirect(reverse('integrated_service:manage'))


@login_required
@check_perms('account.manager', u'无管理权限')
def manager_approve(request):
    app_id = request.GET.get('id')
    app = get_object_or_404(InteServiceApplication, id=app_id)
    if not app.approved:
        for time in app.time:
            if InteServiceApplication.objects.filter(
                place=app.place,
                date=app.date,
                time__contains=time,
                approved=True).exists():
                msg = u'该时间段已经有通过审批的申请'
                return render(request, 'deny.html', {'message': msg})
    app.approved = not app.approved
    app.save()
    return HttpResponseRedirect(reverse('integrated_service:manage'))

