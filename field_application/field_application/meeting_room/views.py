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
        return render(request, 'meeting_room/apply.html', 
                      {'form': MeetingRoomApplicationForm()})

    @method_decorator(login_required)
    def post(self, request):
        form = MeetingRoomApplicationForm(request.POST)
        if not form.is_valid():
            return render(request, 'meeting_room/apply.html', 
                          {'form': form})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('home'))


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
    listing = StudentActivityCenterApplication.objects.filter(organization=org)
    return render(request, 'student_activity_center/manage.html',
                    {'listing': listing})
