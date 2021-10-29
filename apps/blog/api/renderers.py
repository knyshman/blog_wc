from rest_framework.renderers import JSONRenderer


class CustomRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = {
            'error': False,
            'message': 'Success',
            'data': data
        }

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)

from rest_framework.renderers import JSONRenderer

class EmberJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {'element': data}
        return super(EmberJSONRenderer, self).render(data, accepted_media_type, renderer_context)


from rest_framework.renderers import BaseRenderer
from rest_framework.utils import json


class ApiRenderer(BaseRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_dict = {
            'status': 'failure',
            'data': {},
            'message': '',
        }
        if data.get('data'):
            response_dict['data'] = data.get('data')
        if data.get('status'):
            response_dict['status'] = data.get('status')
        if data.get('message'):
            response_dict['message'] = data.get('message')
        data = response_dict
        return json.dumps(data)