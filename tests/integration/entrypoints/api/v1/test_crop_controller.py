import datetime
from typing import TYPE_CHECKING

from fastapi import status

import pytest

from domain.models.auth import Permission

from infrastructure.entrypoints.api.dependencies import get_user

if TYPE_CHECKING:
    import httpx

    from faker import Faker
    from tests.factories.auth_factory import AuthenticatedUserFactory

    from domain.models.auth import AuthenticatedUser

pytestmark = [
    pytest.mark.integration,
    pytest.mark.controller,
    pytest.mark.crop,
]


@pytest.mark.asyncio
async def test_create_crop_miss_required_fields_ko(
    offline_client,
    faker: Faker,
):
    data = {  # Everything but required fields
        'species': 'Ocimum basilicum',
        'description': (
            'Basil (Ocimum basilicum), also called great basil, is a culinary '
            'herb...'
        ),
        'notes': 'Needs water',
    }

    response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


@pytest.mark.asyncio
async def test_create_crop_without_permission_ko(
    offline_app,
    offline_client,
    authenticated_user_factory: type[AuthenticatedUserFactory],
    faker: Faker,
):
    offline_app.dependency_overrides[get_user] = lambda: (
        authenticated_user_factory.build(
            permissions={
                perm for perm in Permission if perm != Permission.WRITE_CROP
            },
        )
    )

    data = {
        'name': 'Basil',
        'planted_at': faker.past_datetime(tzinfo=datetime.UTC).isoformat(),
    }

    response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_create_crop_only_required_fields_ok(
    offline_client,
    faker: Faker,
):
    data = {
        'name': 'Basil',
        'planted_at': faker.past_datetime(tzinfo=datetime.UTC).isoformat(),
    }

    response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_create_crop_all_required_fields_ok(
    offline_client,
    faker: Faker,
):
    data = {
        'name': 'Basil',
        'species': 'Ocimum basilicum',
        'description': (
            'Basil (Ocimum basilicum), also called great basil, is a culinary '
            'herb...'
        ),
        'notes': 'Needs water',
        'planted_at': faker.past_datetime(tzinfo=datetime.UTC).isoformat(),
    }

    response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_get_crop_by_id_not_found_ko(
    offline_client,
    faker: Faker,
):
    response: httpx.Response = offline_client.get(
        url=f'/v1/crops/{faker.uuid4(cast_to=None)}',
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_crop_by_id_without_permission_ko(
    offline_app,
    offline_client,
    authenticated_user_factory: type[AuthenticatedUserFactory],
    faker: Faker,
):
    from infrastructure.entrypoints.api.dependencies import get_user

    offline_app.dependency_overrides[get_user] = lambda: (
        authenticated_user_factory.build(
            permissions={
                perm
                for perm in Permission
                if perm not in {Permission.READ_CROP}
            },
        )
    )

    data = {
        'name': 'Basil',
        'planted_at': faker.past_datetime(tzinfo=datetime.UTC).isoformat(),
    }

    create_response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    response: httpx.Response = offline_client.get(
        url=f'/v1/crops/{create_response.json()["id"]}',
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_get_crop_by_id_ok(
    offline_client,
    faker: Faker,
):
    data = {
        'name': 'Basil',
        'planted_at': faker.past_datetime(tzinfo=datetime.UTC).isoformat(),
    }
    create_response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )
    created_crop_id = create_response.json()['id']

    response: httpx.Response = offline_client.get(
        url=f'/v1/crops/{created_crop_id}',
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_crop_user_without_read_permission_ko(
    offline_app,
    faker: Faker,
    offline_client,
    authenticated_user_factory: type[AuthenticatedUserFactory],
):
    offline_app.dependency_overrides[get_user] = lambda: (
        authenticated_user_factory.build(
            permissions={
                perm for perm in Permission if perm != Permission.READ_CROP
            }
        )
    )

    create_data = {
        'name': 'Basil',
        'planted_at': faker.past_datetime(tzinfo=datetime.UTC).isoformat(),
    }
    create_response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=create_data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )
    created_crop_id = create_response.json()['id']

    data = {
        'name': 'Great Basil',
    }
    response: httpx.Response = offline_client.put(
        url=f'/v1/crops/{created_crop_id}',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_update_crop_user_without_write_permission_ko(
    offline_app,
    faker: Faker,
    offline_client,
    authenticated_user: AuthenticatedUser,
    authenticated_user_factory: type[AuthenticatedUserFactory],
):
    # The user creates the crop with permissions but later on doesn't have them
    # to update
    offline_app.dependency_overrides[get_user] = lambda: authenticated_user
    create_data = {
        'name': 'Basil',
        'planted_at': faker.past_datetime(tzinfo=datetime.UTC).isoformat(),
    }
    create_response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=create_data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )
    created_crop_id = create_response.json()['id']

    offline_app.dependency_overrides[get_user] = lambda: (
        authenticated_user_factory.build(
            id=authenticated_user.id,
            email=authenticated_user.email,
            permissions={
                perm for perm in Permission if perm != Permission.WRITE_CROP
            },
        )
    )
    data = {
        'name': 'Great Basil',
    }
    response: httpx.Response = offline_client.put(
        url=f'/v1/crops/{created_crop_id}',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_update_crop_user_without_ownership_ko(
    offline_app,
    authenticated_user_factory: type[AuthenticatedUserFactory],
    faker: Faker,
    offline_client,
    authenticated_user: AuthenticatedUser,
):
    # The user creates the crop with permissions but later on doesn't have them
    # to update
    offline_app.dependency_overrides[get_user] = lambda: (
        authenticated_user_factory.build()
    )
    create_data = {
        'name': 'Basil',
        'planted_at': faker.past_datetime(tzinfo=datetime.UTC).isoformat(),
    }
    create_response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=create_data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )
    created_crop_id = create_response.json()['id']

    offline_app.dependency_overrides[get_user] = lambda: authenticated_user
    data = {
        'name': 'Great Basil',
    }
    response: httpx.Response = offline_client.put(
        url=f'/v1/crops/{created_crop_id}',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_update_crop_ok(
    offline_app,
    faker: Faker,
    offline_client,
    authenticated_user: AuthenticatedUser,
):
    offline_app.dependency_overrides[get_user] = lambda: authenticated_user
    planted_at = faker.past_datetime(tzinfo=datetime.UTC)
    create_data = {
        'name': 'Basil',
        'planted_at': planted_at.isoformat(),
    }
    create_response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=create_data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )
    created_crop_id = create_response.json()['id']

    data = {
        'name': 'Great Basil',
    }
    response: httpx.Response = offline_client.put(
        url=f'/v1/crops/{created_crop_id}',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['name'] == data['name']
    assert (
        datetime.datetime.fromisoformat(response.json()['planted_at'])
        == planted_at
    )
