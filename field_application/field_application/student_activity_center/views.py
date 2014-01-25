#-*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render, render_to_response
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
from field_application.utils.models import get_second_key
from field_application.student_activity_center.models import \
        StudentActivityCenterApplication


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
            return render(request, 'student_activity_center/apply.html',
                    {'form': form,
                     'post_url': reverse('student_activity_center:apply')})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('home'))


def display_table(request):
    week = int(request.GET.get('week') or 0)
    table = StudentActivityCenterApplication.generate_table(offset=week)
    return render(request, 'student_activity_center/table.html',
                  {'table': table, 'curr_week': week})


def display_listing(request):
    listing = StudentActivityCenterApplication.objects.all()
    for app in listing:
        app.place = get_second_key(app.place,
                StudentActivityCenterApplication.PLACE)
        app.time = get_second_key(app.time,
                StudentActivityCenterApplication.TIME)
    paginator = Paginator(listing, 3)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return render(request, 'student_activity_center/listing.html',
                  {'page': page})


@login_required
def manage(request):
    org = request.user.organization
    listing = StudentActivityCenterApplication.objects.\
            filter(organization=org).order_by('-pk')
    paginator = Paginator(listing, 3)
    for app in listing:
        app.time = get_second_key(app.time,
                StudentActivityCenterApplication.TIME)
        app.place = get_second_key(app.place,
                StudentActivityCenterApplication.PLACE)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return render(request, 'student_activity_center/manage.html',
            {'page': page})

 
def get_detail(request):
    app = StudentActivityCenterApplication.objects.get(
            id=request.GET.get('id'))
    time = [get_second_key(t, StudentActivityCenterApplication.TIME) \
                for t in app.time]
    data = {'organization': app.organization.chinese_name,
            'place': app.place,
            'date': app.date.strftime('%Y年%m月%d日'),
            'time': time, 'activity': app.activity,
            'approved': app.approved, 'plan_file': app.plan_file.url,
            'applicant_name': app.applicant_name,
            'applicant_phone_number': app.applicant_phone_number,
            'application_time': \
                    app.application_time.strftime('%Y年%m月%d日 %H:%M:%S'),
            'sponsor': app.sponsor, 'sponsorship': app.sponsorship,
            'sponsorship_usage': app.sponsorship_usage,
            'activity_summary': app.activity_summary,
            'remarks': app.remarks }
    return render_json(data)

class ModifyView(View):

    @method_decorator(login_required)
    def get(self, request):
        app_id = request.GET.get('id')
        app = StudentActivityCenterApplication.objects.get(id=app_id)
        form = StudentActivityCenterApplicationForm(instance=app)
        return render(request, 'student_activity_center/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': \
                     reverse('student_activity_center:modify')+'?id='+app_id})

    @method_decorator(login_required)
    def post(self, request):
        app_id = request.GET.get('id')
        app = StudentActivityCenterApplication.objects.get(id=app_id)
        form = StudentActivityCenterApplicationForm(
                request.POST, request.FILES, instance=app)
        if not form.is_valid():
            return render(request, 'student_activity_center/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': \
                     reverse('student_activity_center:modify')+'?id='+app_id})
        form.save()
        return HttpResponseRedirect(reverse('student_activity_center:manage'))
