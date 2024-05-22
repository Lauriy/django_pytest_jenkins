from django.db.models import Model, DateTimeField, CharField


class Stuff(Model):
    name = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
