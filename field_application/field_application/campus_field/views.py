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
from field_application.campus_field.forms import PublicityApplicationForm
from field_application.campus_field.models import ExhibitApplication
from field_application.campus_field.models import PublicityApplication
from field_application.utils.models import get_second_key


class ApplyExhibitView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'campus_field/apply-exhibit.html', 
                      {'form': ExhibitApplicationForm()})

    @method_decorator(login_required)
    def post(self, request):
        form = ExhibitApplicationForm(request.POST,
                                      request.FILES)
        if not form.is_valid():
            return render(request, 'campus_field/apply-exhibit.html', 
                          {'form': form})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('campus_field:exhibit_table'))


class ApplyPublicityView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'campus_field/apply-publicity.html', 
                      {'form': PublicityApplicationForm()})

    @method_decorator(login_required)
    def post(self, request):
        form = PublicityApplicationForm(request.POST,
                                        request.FILES)
        if not form.is_valid():
            return render(request, 'campus_field/apply-publicity.html', 
                          {'form': form})
        app = form.save(commit=False)
        app.organization = request.user.organization
        app.save()
        return HttpResponseRedirect(reverse('home'))


def display_exhibit_table(request):
    week = int(request.GET.get('week') or 0)
    table = ExhibitApplication.generate_table(offset=week)
    return render(request, 'campus_field/exhibit_table.html',
            {'table': table, 'curr_week': week})


def display_exhibit_list(request):
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
    return render(request, 'campus_field/exhibit_list.html',
                  {'page': page})


def display_publicity_table(request):
    week = int(request.GET.get('week') or 0)
    table = PublicityApplication.generate_table(offset=week)
    return render(request, 'campus_field/publicity_table.html',
            {'table': table, 'curr_week': week})


def display_publicity_list(request):
    listing = PublicityApplication.objects.all()
    for app in listing:
        for i in range(len(app.place)):
            app.place[i] = get_second_key(app.place[i],
                    PublicityApplication.PLACE)
        for i in range(len(app.time)):
            app.time[i] = get_second_key(app.time[i],
                    PublicityApplication.TIME)
    paginator = Paginator(listing, 3)
    try:
        page = paginator.page(request.GET.get('page'))
    except InvalidPage:
        page = paginator.page(1)
    return render(request, 'campus_field/publicity_list.html',
                  {'page': page})
