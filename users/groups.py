from django.contrib.auth.models import Group

from .models import User

moderator_group = Group.objects.create(name='Moderators')

user = User.objects.get(username='admin')
user.groups.add(moderator_group)
