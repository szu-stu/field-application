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

from field_application.meeting_room.forms import MeetingRoomApplicationForm
from field_application.meeting_room.models import MeetingRoomApplication
from field_application.utils.models import get_second_key


class ApplyMeetingRoomView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'meeting_room/form.html', 
                      {'form': MeetingRoomApplicationForm(),
                       'post_url': reverse('meeting_room:apply')})

    @method_decorator(login_required)
    def post(self, request):
        form = MeetingRoomApplicationForm(request.POST)
        if not form.is_valid():
            return render(request, 'meeting_room/form.html', 
                          {'form': form,
                           'post_url': reverse('meeting_room:apply')})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('meeting_room:table'))


def display_table(request):
    week = int(request.GET.get('week') or 0)
    table = MeetingRoomApplication.generate_table(offset=week)
    return render(request, 'meeting_room/table.html',
            {'table': table, 'curr_week': week})


def display_listing(request):
    listing = MeetingRoomApplication.objects.all()
    for app in listing:
        app.place = get_second_key(app.place,
                MeetingRoomApplication.PLACE)
        for i in range(len(app.time)):
            app.time[i] = get_second_key(app.time[i],
                    MeetingRoomApplication.TIME)
    paginator = Paginator(listing, 3)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return render(request, 'meeting_room/listing.html',
                  {'page': page})


@login_required
def manage(request):
    org = request.user.organization
    listing = MeetingRoomApplication.objects.\
            filter(organization=org).order_by('-pk')
    paginator = Paginator(listing, 3)
    for app in listing:
        for i in range(len(app.time)):
            app.time[i] = get_second_key(app.time[i],
                    MeetingRoomApplication.TIME)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return render(request, 'meeting_room/manage.html',
            {'page': page})

 
def get_detail(request):
    app = MeetingRoomApplication.objects.get(id=request.GET.get('id'))
    time = [get_second_key(t, MeetingRoomApplication.TIME) \
                for t in app.time]
    data = {'organization': app.organization.chinese_name,
            'place': app.place,
            'date': app.date.strftime('%Y年%m月%d日'),
            'time': time, 'meeting_topic': app.meeting_topic,
            'approved': app.approved, 'applicant_name': app.applicant_name,
            'applicant_phone_number': app.applicant_phone_number,
            'application_time': \
                    app.application_time.strftime('%Y年%m月%d日 %H:%M:%S'),
            'meeting_summary': app.activity_summary,
            'remarks': app.remarks }
    return render_json(data)


class ModifyView(View):

    @method_decorator(login_required)
    def get(self, request):
        app_id = request.GET.get('id')
        app = MeetingRoomApplication.objects.get(id=app_id)
        form = MeetingRoomApplicationForm(instance=app)
        return render(request, 'meeting_room/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': reverse('meeting_room:modify')+'?id='+app_id})

    @method_decorator(login_required)
    def post(self, request):
        app_id = request.GET.get('id')
        app = MeetingRoomApplication.objects.get(id=app_id)
        form = MeetingRoomApplicationForm(request.POST, instance=app)
        if not form.is_valid():
            return render(request, 'meeting_room/form.html', 
                {'form': form, 'app_id': app_id,
                 'post_url': reverse('meeting_room:modify')+'?id='+app_id})
        form.save()
        return HttpResponseRedirect(reverse('meeting_room:manage'))
