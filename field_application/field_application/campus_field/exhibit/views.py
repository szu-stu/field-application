#-*- coding: utf-8 -*-
import logging

from django.views.generic import View
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.forms import NON_FIELD_ERRORS
from django.core.paginator import InvalidPage, Paginator

from field_application.campus_field.forms import ExhibitApplicationForm
from field_application.campus_field.models import ExhibitApplication
from field_application.utils.models import get_second_key


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
        return HttpResponseRedirect(reverse('exhibit:table'))


def display_table(request):
    week = int(request.GET.get('week') or 0)
    table = ExhibitApplication.generate_table(offset=week)
    return render(request, 'campus_field/exhibit/table.html',
            {'table': table, 'curr_week': week})


def display_list(request):
    listing = ExhibitApplication.objects.all()
    for app in listing:
        for i in range(len(app.place)):
            app.place[i] = get_second_key(app.place[i],
                    ExhibitApplication.PLACE)
        for i in range(len(app.time)):
            app.time[i] = get_second_key(app.time[i],
                    ExhibitApplication.TIME)
    paginator = Paginator(listing, 3)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return render(request, 'campus_field/exhibit/list.html',
                  {'page': page})


@login_required
def manage(request):
    org = request.user.organization
    listing = ExhibitApplication.objects.\
            filter(organization=org).order_by('-pk')
    paginator = Paginator(listing, 3)
    for app in listing:
        app.time = [get_second_key(time, ExhibitApplication.TIME) \
                        for time in app.time ]
        app.place = [ get_second_key(place, ExhibitApplication.PLACE) \
                        for place in app.place ]
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return render(request, 'campus_field/exhibit/manage.html',
            {'page': page})

 
def get_detail(request):
    app = ExhibitApplication.objects.get(
            id=request.GET.get('id'))
    data = {'organization': app.organization.chinese_name,
            'place': get_second_key(app.place,
                ExhibitApplication.PLACE),
            'date': app.date.strftime('%Y年%m月%d日'),
            'time': get_second_key(app.time,
                ExhibitApplication.TIME),
            'activity': app.activity,
            'approved': app.approved, 'plan_file': app.plan_file.url,
            'applicant_name': app.applicant_name,
            'applicant_phone_number': app.applicant_phone_number,
            'application_time': \
                    app.application_time.strftime('%Y年%m月%d日 %H:%M:%S'),
            'sponsor': app.sponsor, 'sponsorship': app.sponsorship,
            'sponsorship_usage': app.sponsorship_usage,
            'activity_summary': app.activity_summary}
    return render_json(data)


class ModifyView(View):

    @method_decorator(login_required)
    def get(self, request):
        app_id = request.GET.get('id')
        app = ExhibitApplication.objects.get(id=app_id)
        form = ExhibitApplicationForm(instance=app)
        return render(request, 'campus_field/exhibit/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': \
                     reverse('exhibit:modify')+'?id='+app_id})

    @method_decorator(login_required)
    def post(self, request):
        app_id = request.GET.get('id')
        app = ExhibitApplication.objects.get(id=app_id)
        form = ExhibitApplicationForm(
                request.POST, request.FILES, instance=app)
        if not form.is_valid():
            return render(request, 'campus_field/exhibit/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': \
                     reverse('exhibit:modify')+'?id='+app_id})
        form.save()
        return HttpResponseRedirect(reverse('exhibit:manage'))
