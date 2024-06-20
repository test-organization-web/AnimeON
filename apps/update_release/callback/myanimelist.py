from django.http import JsonResponse
from django.core.management import call_command


def callback(request):
    if 'code' not in request.GET:
        return JsonResponse(data={})
    call_command('myanimelist_update_releases', authorisation_code=request.GET['code'])
    return JsonResponse(data={})
