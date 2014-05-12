#-*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.forms import NON_FIELD_ERRORS
from django.core.paginator import InvalidPage, Paginator

from field_application.student_activity_center.forms \
        import StudentActivityCenterApplicationForm
from field_application.student_activity_center.models \
        import StudentActivityCenterApplication
from field_application.student_activity_center.models import \
        StudentActivityCenterApplication
from field_application.utils.ajax import render_json
from field_application.account.permission import check_perms, check_ownership
from field_application.account.permission import check_not_approved
from field_application.utils.forms import SearchForm
from field_application.utils.views import search_application 


class ApplyView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 
                      'student_activity_center/form.html', 
                      {'form': StudentActivityCenterApplicationForm(),
                       'post_url': reverse('student_activity_center:apply')})

    @method_decorator(login_required)
    def post(self, request):
        form = StudentActivityCenterApplicationForm(request.POST,
                                                    request.FILES)
        if not form.is_valid():
            return render(request, 'student_activity_center/form.html',
                    {'form': form,
                     'post_url': reverse('student_activity_center:apply')})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('student_activity_center:manage'))


def display_table(request):
    week = int(request.GET.get('week') or 0)
    table = StudentActivityCenterApplication.generate_table(offset=week)
    return render(request, 'student_activity_center/table.html',
                  {'table': table, 'curr_week': week})


def generate_page(listing, request):
    for app in listing:
        app.date = app.date.strftime('%Y年%m月%d日')
        app.place = [app.place]
        app.time = app.time
    paginator = Paginator(listing, 40)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return page


class ListAppView(View):

    def get(self, request):
        listing = StudentActivityCenterApplication.objects.all().order_by('-pk')
        return render(request, 'list.html',
                    {'page': generate_page(listing, request),
                     'title': u'学生活动中心场地申请',
                     'form': SearchForm()})

    def post(self, request):
        form = SearchForm(request.POST)
        if not form.is_valid():
            listing = \
                StudentActivityCenterApplication.objects.all().order_by('-pk')
        else:
            listing = search_application(StudentActivityCenterApplication,
                                         form).order_by('-pk')
        return render(request, 'list.html',
                    {'page': generate_page(listing, request),
                     'title': u'学生活动中心场地申请',
                     'form': form})


class ManageView(View):

    @method_decorator(login_required)
    def get(self, request):
        return ManageView.manage(request,
            StudentActivityCenterApplication.objects.all(),
            SearchForm())

    @method_decorator(login_required)
    def post(self, request):
        form = SearchForm(request.POST)
        if not form.is_valid():
            listing = \
                StudentActivityCenterApplication.objects.all().order_by('-pk')
        else:
            listing = search_application(StudentActivityCenterApplication,
                                         form)
        return ManageView.manage(request, listing, form)

    @classmethod
    def manage(cls, request, listing, form):
        org = request.user.organization
        if org.user.has_perm('account.manager'):
            listing = \
                listing.order_by('-pk')
        else:
            listing = listing.filter(organization=org).order_by('-pk')
        page = generate_page(listing, request)
        return render(request, 'manage.html',
                {'page': page, 'title': u'学生活动中心场地申请',
                 'modify_url': reverse('student_activity_center:modify'),
                 'approve_url': \
                         reverse('student_activity_center:manager_approve'),
                 'delete_url': \
                         reverse('student_activity_center:delete'),
                 'form': form})
 

def get_detail(request):
    app_id = request.GET.get('id')
    app = get_object_or_404(StudentActivityCenterApplication, id=app_id)
    data = {'organization': app.organization.chinese_name,
            'place': app.place,
            'date': app.date.strftime('%Y年%m月%d日'),
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
            'id': app_id,
            'user_is_manager': request.user.has_perm('account.manager')}
    return render_json(data)

class ModifyView(View):

    @method_decorator(login_required)
    @method_decorator(check_ownership(StudentActivityCenterApplication))
    @method_decorator(check_not_approved(StudentActivityCenterApplication))
    def get(self, request):
        app_id = request.GET.get('id')
        app = get_object_or_404(StudentActivityCenterApplication, id=app_id)
        form = StudentActivityCenterApplicationForm(instance=app)
        return render(request, 'student_activity_center/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': \
                     reverse('student_activity_center:modify')+'?id='+app_id})

    @method_decorator(login_required)
    @method_decorator(check_ownership(StudentActivityCenterApplication))
    @method_decorator(check_not_approved(StudentActivityCenterApplication))
    def post(self, request):
        app_id = request.GET.get('id')
        app = get_object_or_404(StudentActivityCenterApplication, id=app_id)
        form = StudentActivityCenterApplicationForm(
                request.POST, request.FILES, instance=app)
        if not form.is_valid():
            return render(request, 'student_activity_center/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': \
                     reverse('student_activity_center:modify')+'?id='+app_id})
        form.save()
        return HttpResponseRedirect(reverse('student_activity_center:manage'))


@login_required
@check_ownership(StudentActivityCenterApplication)
@check_not_approved(StudentActivityCenterApplication)
def delete(request):
    app_id = request.GET.get('id')
    app = get_object_or_404(StudentActivityCenterApplication, id=app_id)
    app.delete()
    return HttpResponseRedirect(reverse('student_activity_center:manage'))


@login_required
@check_perms('account.manager', u'无管理权限')
def manager_approve(request):
    app_id = request.GET.get('id')
    app = get_object_or_404(StudentActivityCenterApplication, id=app_id)
    app.approved = not app.approved
    app.save()
    return HttpResponseRedirect(reverse('student_activity_center:manage'))

