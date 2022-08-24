from django.db.models.signals import post_save

from django.dispatch import receiver

from core.models import (User, Account)


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    print('create account running')
    if created:
        user_account = Account(user=instance)
        user_account.save()
        user_account.name = instance.name
        user_account.friends.add(instance.account)
        user_account.save()
