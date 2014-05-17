from field_application.utils.forms import SearchForm
from field_application.meeting_room.models import MeetingRoomApplication
from field_application.campus_field.models import PublicityApplication
from field_application.campus_field.models import ExhibitApplication
from django.db.models import Q


def search_application(model, form):
    search_type = form.cleaned_data['search_type']
    search_value = form.cleaned_data['search_value']
    approved_value = form.cleaned_data['approved']

    search_value = '%' + '%'.join(search_value) + '%' 
    if search_type == 'org':
        apps = model.objects.filter(
                organization__chinese_name__like=search_value)
    elif search_type == 'title':
        if model == MeetingRoomApplication:
            apps = model.objects.filter(meeting_topic__like=search_value)
        else:
            apps = model.objects.filter(activity__like=search_value)
    elif search_type == 'place':
        if model == PublicityApplication:
            apps = model.objects.filter(
                Q(other_place__like=search_value) | Q(place__like=search_value))
        else:
            apps = model.objects.filter(place__like=search_value)
    else:
        raise Exception('search_type is not valid')

    if approved_value == 'all':
        return apps
    elif approved_value == 'yes':
        return apps.filter(approved=True)
    elif approved_value == 'no':
        return apps.filter(approved=False)
    else:
        raise Exception('approved_value is not valid')

