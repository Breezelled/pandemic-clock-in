from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers


class Response:
    def JsonResponse(data):
        if data is not None:
            result = []
            data_dict = json.loads(serializers.serialize('json', data))
            for d in data_dict:
                result.append(d['fields'])
            result = {'code': 0, 'data': result}
        else:
            result = {'data': None}
        return JsonResponse(result)
