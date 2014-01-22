import logging

from django.views.generic import View
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.forms import NON_FIELD_ERRORS

from field_application.meeting_room.forms import MeetingRoomApplicationForm
from field_application.meeting_room.models import MeetingRoomApplication


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
    return render(request, 'meeting_room/listing.html',
                  {'listing': listing})
