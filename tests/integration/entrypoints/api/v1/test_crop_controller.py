from typing import TYPE_CHECKING

from fastapi import status

import pytest

from domain.models.auth import Permission

if TYPE_CHECKING:
    from faker import Faker
    from tests.factories.auth_factory import AuthenticatedUserFactory

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
        'unique_name': 'Ocimum basilicum',
        'description': (
            'Basil (Ocimum basilicum), also called great basil, is a culinary '
            'herb...'
        ),
        'notes': 'Needs water',
    }

    response = offline_client.post(
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
    from infrastructure.entrypoints.api.dependencies import get_user

    offline_app.dependency_overrides[get_user] = lambda: (
        authenticated_user_factory(
            permissions={
                perm
                for perm in Permission
                if perm not in {Permission.WRITE_CROP}
            },
        )
    )

    data = {
        'name': 'Basil',
    }

    response = offline_client.post(
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
    }

    response = offline_client.post(
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
        'unique_name': 'Ocimum basilicum',
        'description': (
            'Basil (Ocimum basilicum), also called great basil, is a culinary '
            'herb...'
        ),
        'notes': 'Needs water',
    }

    response = offline_client.post(
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
    response = offline_client.get(
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
        authenticated_user_factory(
            permissions={
                perm
                for perm in Permission
                if perm not in {Permission.READ_CROP}
            },
        )
    )

    data = {
        'name': 'Basil',
    }

    create_response = offline_client.post(
        url='/v1/crops',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    response = offline_client.get(
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
    }

    create_response = offline_client.post(
        url='/v1/crops',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    response = offline_client.get(
        url=f'/v1/crops/{create_response.json()["id"]}',
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_200_OK
