from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.db import transaction

from developers.models import Developer
from assets.models import Asset
from licenses.models import License


@receiver(pre_save, sender=Developer)
@transaction.atomic()
def deactivate_related_assets_and_licenses(sender, instance, **kwargs):
    if instance.id is not None:
        orig = Developer.objects.get(pk=instance.id)
        if orig.active and not instance.active:
            Asset.objects.filter(assigned_to=instance).update(assigned_to=None)
            License.objects.filter(assigned_to=instance).update(assigned_to=None)


@receiver(pre_delete, sender=Developer)
def unassign_assets(sender, instance, **kwargs):
    Asset.objects.filter(assigned_to=instance).update(assigned_to=None)
    License.objects.filter(assigned_to=instance).update(assigned_to=None)