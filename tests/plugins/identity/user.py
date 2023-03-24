from typing import TypedDict, final, Callable

import faker
import pytest
from mixer.backend.django import mixer
from typing_extensions import TypeAlias

from server.apps.identity.models import User

fake = faker.Faker()


class UserCredentials(TypedDict):
    email: str
    password1: str
    password2: str


class UserData(TypedDict):
    first_name: str
    last_name: str
    date_of_birth: str
    address: str
    job_title: str
    phone: str


@pytest.fixture
def user_credentials() -> UserCredentials:
    password = fake.password()
    data = {
        "email": fake.email(),
        "password1": password,
        "password2": password,
    }
    return UserCredentials(**data)


@pytest.fixture
def user_data() -> UserData:
    return UserData(
        **{
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "date_of_birth": fake.date_of_birth(),
            "address": fake.address(),
            "job_title": fake.job(),
            "phone": fake.phone_number(),
        }
    )


UserAssertion: TypeAlias = Callable[[UserCredentials, UserData], None]


@pytest.fixture
def assert_user_was_created() -> UserAssertion:
    def factory(user_credentials: UserCredentials, user_data: UserData) -> None:
        user = User.objects.get(email=user_credentials['email'])
        assert user.id
        assert user.check_password(user_credentials['password1'])
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_anonymous
        assert user.is_authenticated
        for field in user.REQUIRED_FIELDS:
            assert getattr(user, field) == user_data[field]

    return factory


@pytest.fixture
def user():
    return mixer.blend(User)
