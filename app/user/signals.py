from django.db.models.signals import post_save

from django.dispatch import receiver

from core.models import (User, Account, Friend)


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):

    if created:
        user_account = Account(user=instance)
        user_account.save()
        user_account.name = instance.name
        self_friend = Friend(user=instance)
        self_friend.save()
        user_account.friends.add(self_friend)
        user_account.save()
