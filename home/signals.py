from .models import Provider, Visit
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from time import strftime
import pytz, datetime

local_tz = pytz.timezone('Europe/Warsaw')

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary

@receiver(post_save, sender=Visit)
def announce_new_visit(sender, instance, created, **kwargs):

    if created:
        channel_layer = get_channel_layer()

        #Convert timezone to local from UTC:
        timeLocal = utc_to_local(instance.dateOfVisit)

        async_to_sync(channel_layer.group_send)(
            'gossip', {
                'type': 'user.gossip',
                'event': 'New Visit',
                'provider': instance.provider.shortcut,
                'providerName': instance.provider.name,
                'date_and_time': timeLocal.strftime('%d.%m.%y, %H:%M'),
                'floor': instance.floor,
            }
        )
        print('Wyslano')