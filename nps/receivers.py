from django.dispatch import receiver

from nps.services.nps import nps_update
from nps.signals import nps_inserted

from utils.requests import get_metadata


@receiver(nps_inserted)
def add_metadata_to_nps(sender, nps_id, request, **kwargs):
    nps_update(id=nps_id, metadata=get_metadata(request))
