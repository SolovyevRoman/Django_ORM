from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import format_duration
from django.shortcuts import render


def storage_information_view(request):
    # Программируем здесь
    visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for current in visits:
        pass_current = current.passcard
        info_visit = {'who_entered': pass_current.owner_name, 'entered_at':
                      current.entered_at, 'duration': format_duration(current.get_duration())}
        non_closed_visits.append(info_visit)

    #non_closed_visits = [
    #    {
    #        'who_entered': 'Richard Shaw',
    #        'entered_at': '11-04-2018 25:34',
    #        'duration': '25:03',
    #    }
    #]
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
