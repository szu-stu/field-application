#-*- coding: utf-8 -*-
from django.views.generic import View
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.forms import NON_FIELD_ERRORS
from django.core.paginator import InvalidPage, Paginator

from field_application.south_stadium.forms import SouthStadiumApplicationForm
from field_application.south_stadium.models import SouthStadiumApplication
from field_application.utils.models import get_second_key
from field_application.utils.ajax import render_json


class ApplyView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'south_stadium/form.html', 
                      {'form': SouthStadiumApplicationForm()})

    @method_decorator(login_required)
    def post(self, request):
        form = SouthStadiumApplicationForm(request.POST,
                                           request.FILES)
        if not form.is_valid():
            return render(request, 'south_stadium/form.html',
                          {'form': form})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('home'))


def display_table(request):
    week = int(request.GET.get('week') or 0)
    table = SouthStadiumApplication.generate_table(offset=week)
    return render(request, 'south_stadium/table.html',
                  {'table': table, 'curr_week': week})


def display_listing(request):
    listing = SouthStadiumApplication.objects.all()
    for app in listing:
        for i in range(len(app.time)):
            app.time[i] = get_second_key(app.time[i],
                    SouthStadiumApplication.TIME)
    paginator = Paginator(listing, 3)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return render(request, 'south_stadium/listing.html',
                  {'page': page})


@login_required
def manage(request):
    org = request.user.organization
    listing = SouthStadiumApplication.objects.\
            filter(organization=org).order_by('-pk')
    paginator = Paginator(listing, 3)
    for app in listing:
        for i in range(len(app.time)):
            app.time[i] = get_second_key(app.time[i],
                    SouthStadiumApplication.TIME)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return render(request, 'south_stadium/manage.html',
            {'page': page})


class ModifyView(View):

    @method_decorator(login_required)
    def get(self, request):
        app_id = request.GET.get('id')
        app = SouthStadiumApplication.objects.get(id=app_id)
        form = SouthStadiumApplicationForm(instance=app)
        return render(request, 'south_stadium/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': reverse('south_stadium:modify')+'?id='+app_id})

    @method_decorator(login_required)
    def post(self, request):
        app_id = request.GET.get('id')
        app = SouthStadiumApplication.objects.get(id=app_id)
        form = SouthStadiumApplicationForm(request.POST, request.FILES,
                                           instance=app)
        if not form.is_valid():
            return render(request, 'south_stadium/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': reverse('south_stadium:modify')+'?id='+app_id})
        form.save()
        return HttpResponseRedirect(reverse('south_stadium:manage'))


def message(request):
    app = SouthStadiumApplication.objects.get(id=request.GET.get('id'))
    time = [get_second_key(t, SouthStadiumApplication.TIME) \
                for t in app.time]
    data = {'organization': app.organization.chinese_name,
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
