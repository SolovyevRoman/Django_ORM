from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import format_duration
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime


def passcard_info_view(request, passcode):
    #passcard = Passcard.objects.all()[0]
    # Программируем здесь
    this_passcard_visits = []

    #passcard = Passcard.objects.get(passcode=passcode)
    passcard = get_object_or_404(Passcard, passcode=passcode)
    
    visits = Visit.objects.filter(passcard=passcard)

    for current_visit in visits:
        info_visit = { 'entered_at': localtime(current_visit.entered_at),
                       'duration': format_duration(current_visit.get_duration()),
                       'is_strange': current_visit.is_visit_long }
        this_passcard_visits.append(info_visit)
    
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
