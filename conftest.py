import factory
import pytest
from faker import Faker

from common_app.models import Stuff

fake = Faker()


class StuffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stuff

    name = factory.LazyAttribute(lambda _: fake.name())


@pytest.fixture
def stuff_instance():
    return StuffFactory.create()
