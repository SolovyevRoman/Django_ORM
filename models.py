import time

from django.db import models

from datetime import datetime, timedelta

def format_duration(duration):
    result = time.gmtime(duration)
    return f'{result.tm_hour}ч. {result.tm_min}мин.'
    #return time.strftime("%H:%M:%S", time.gmtime(duration)) 

class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        end_date = datetime.now()
        if self.leaved_at != None:
            period = self.leaved_at - self.entered_at
        else:
            period = end_date - self.entered_at.replace(tzinfo=None)
        return period.total_seconds()

    def is_visit_long(self, minutes=60):
        end_date = datetime.now()
        if self.leaved_at != None:
            period = self.leaved_at - self.entered_at
            result = time.gmtime(period.total_seconds())
            if (result.tm_hour*60+result.tm_min) >= minutes:
                return True
        else:
            period = end_date - self.entered_at.replace(tzinfo=None)
            result = time.gmtime(period.total_seconds())
            if (result.tm_hour*60+result.tm_min) >= check_time_min:
                return True
        return False
                
