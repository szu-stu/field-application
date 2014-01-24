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
                      'student_activity_center/apply.html', 
                      {'form': StudentActivityCenterApplicationForm()})

    @method_decorator(login_required)
    def post(self, request):
        form = StudentActivityCenterApplicationForm(request.POST,
                                                    request.FILES)
        if not form.is_valid():
            return render(request, 'student_activity_center/apply.html',
                          {'form': form})
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
    listing = StudentActivityCenterApplication.objects.filter(organization=org)

    return render(request, 'student_activity_center/manage.html',
                    {'listing': listing})
