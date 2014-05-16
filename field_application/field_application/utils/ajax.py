import json
import urllib2

from django.http import HttpResponse


def render_json(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


def spec_json(status='Error', messages=None):
    if not messages:
        messages = []
    elif not isinstance(messages, (dict, list, tuple)):
        messages = [messages]
    data = {'status': status, 'messages': messages}
    return render_json(data)
