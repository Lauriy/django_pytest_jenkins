from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from common_app.models import Stuff


def do_stuff(request, stuff_id: int):
    thing = get_object_or_404(Stuff, pk=stuff_id)
    thing.save()

    return JsonResponse({
        'id': thing.id,
        'name': thing.name,
        'updatedAt': thing.updated_at,
    })
