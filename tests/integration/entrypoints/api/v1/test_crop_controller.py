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
    from tests.factories.crop_factory import CropFactory

    from domain.models.auth import AuthenticatedUser
    from domain.models.crop import Crop

pytestmark = [
    pytest.mark.integration,
    pytest.mark.controller,
    pytest.mark.crop,
]


def test_create_crop_miss_required_fields_ko(
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


def test_create_crop_user_without_write_permission_ko(
    offline_app,
    offline_client,
    authenticated_user_factory: type[AuthenticatedUserFactory],
    faker: Faker,
):
    offline_app.dependency_overrides[get_user] = lambda: (
        authenticated_user_factory.build(
            permissions={
                perm
                for perm in Permission
                if perm not in {Permission.WRITE_CROPS, Permission.WRITE_ALL}
            },
        )
    )

    data = {
        'name': 'Basil',
        'planted_at': faker.date_time(tzinfo=datetime.UTC).isoformat(),
    }

    response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert (
        response.json()['detail']
        == 'Not enough permissions to perform this action.'
    )


def test_create_crop_only_required_fields_ok(
    offline_client,
    faker: Faker,
):
    data = {
        'name': 'Basil',
        'planted_at': faker.date_time(tzinfo=datetime.UTC).isoformat(),
    }

    response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_create_crop_all_required_fields_ok(
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
        'planted_at': faker.date_time(tzinfo=datetime.UTC).isoformat(),
    }

    response: httpx.Response = offline_client.post(
        url='/v1/crops',
        json=data,
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED


def test_get_crop_by_id_not_found_ko(
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
    assert response.json()['message'] == 'Crop not found.'


def test_get_crop_by_id_user_without_read_permission_ko(
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
                if perm not in {Permission.READ_CROPS, Permission.READ_ALL}
            },
        )
    )

    data = {
        'name': 'Basil',
        'planted_at': faker.date_time(tzinfo=datetime.UTC).isoformat(),
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
    assert (
        response.json()['detail']
        == 'Not enough permissions to perform this action.'
    )


def test_get_crop_by_id_ok(
    offline_client,
    faker: Faker,
):
    data = {
        'name': 'Basil',
        'planted_at': faker.date_time(tzinfo=datetime.UTC).isoformat(),
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
    assert response.json()['id'] == created_crop_id


def test_update_crop_user_without_read_permission_ko(
    offline_app,
    faker: Faker,
    offline_client,
    authenticated_user_factory: type[AuthenticatedUserFactory],
):
    offline_app.dependency_overrides[get_user] = lambda: (
        authenticated_user_factory.build(
            permissions={
                perm
                for perm in Permission
                if perm not in {Permission.READ_CROPS, Permission.READ_ALL}
            }
        )
    )

    create_data = {
        'name': 'Basil',
        'planted_at': faker.date_time(tzinfo=datetime.UTC).isoformat(),
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
    assert (
        response.json()['detail']
        == 'Not enough permissions to perform this action.'
    )


def test_update_crop_user_without_write_permission_ko(
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
        'planted_at': faker.date_time(tzinfo=datetime.UTC).isoformat(),
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
                perm
                for perm in Permission
                if perm not in {Permission.WRITE_CROPS, Permission.WRITE_ALL}
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
    assert (
        response.json()['detail']
        == 'Not enough permissions to perform this action.'
    )


def test_update_crop_user_without_ownership_ko(
    offline_app,
    authenticated_user_factory: type[AuthenticatedUserFactory],
    faker: Faker,
    offline_client,
    authenticated_user: AuthenticatedUser,
):
    # One user creates the crop and another user tries to update it without
    # ownership
    offline_app.dependency_overrides[get_user] = lambda: (
        authenticated_user_factory.build()
    )
    create_data = {
        'name': 'Basil',
        'planted_at': faker.date_time(tzinfo=datetime.UTC).isoformat(),
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
    assert (
        response.json()['message']
        == "User doesn't have ownership of this crop."
    )


def test_update_crop_ok(
    offline_app,
    faker: Faker,
    offline_client,
    authenticated_user: AuthenticatedUser,
):
    offline_app.dependency_overrides[get_user] = lambda: authenticated_user
    planted_at = faker.date_time(tzinfo=datetime.UTC)
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


def test_list_crops_user_without_read_permissions_ko(
    offline_app,
    authenticated_user_factory: type[AuthenticatedUserFactory],
    offline_client,
    faker: Faker,
):
    offline_app.dependency_overrides[get_user] = lambda: (
        authenticated_user_factory.build(
            permissions={
                perm
                for perm in Permission
                if perm not in {Permission.READ_CROPS, Permission.READ_ALL}
            }
        )
    )

    response: httpx.Response = offline_client.get(
        url='/v1/crops',
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert (
        response.json()['detail']
        == 'Not enough permissions to perform this action.'
    )


@pytest.mark.asyncio
async def test_list_crops_without_query_params_ok(
    offline_app,
    authenticated_user: AuthenticatedUser,
    in_memory_crop_repo,
    crop_factory: type[CropFactory],
    offline_client,
    faker: Faker,
):
    offline_app.dependency_overrides[get_user] = lambda: authenticated_user
    n_items = 15
    for crop in crop_factory.build_batch(
        size=n_items,
        owner_id=authenticated_user.id,
    ):
        await in_memory_crop_repo.save(crop=crop)

    response: httpx.Response = offline_client.get(
        url='/v1/crops',
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == n_items


@pytest.mark.asyncio
async def test_list_crops_with_query_params_ok(
    offline_app,
    authenticated_user: AuthenticatedUser,
    in_memory_crop_repo,
    crop_factory: type[CropFactory],
    offline_client,
    faker: Faker,
):
    offline_app.dependency_overrides[get_user] = lambda: authenticated_user
    n_items = 15
    for crop in crop_factory.build_batch(
        size=n_items,
        owner_id=authenticated_user.id,
    ):
        await in_memory_crop_repo.save(crop=crop)
    crop_planted_at = faker.date_time(tzinfo=datetime.UTC)
    crop = crop_factory.build(
        name='Basil',
        species='Ocimum basilicum',
        description=(
            'Basil (Ocimum basilicum), also called great basil, is a culinary '
            'herb...'
        ),
        notes='Needs water.',
        planted_at=crop_planted_at,
        owner_id=authenticated_user.id,
    )
    await in_memory_crop_repo.save(crop=crop)

    response: httpx.Response = offline_client.get(
        url='/v1/crops',
        params={
            'name': 'basil',
            'species': 'basilicum',
            'description': 'also called great basil',
            'notes': 'water',
            'planted_at': crop_planted_at.isoformat(),
        },
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == 1


@pytest.mark.asyncio
async def test_list_crops_only_owned_ok(
    offline_app,
    authenticated_user: AuthenticatedUser,
    crop_factory: type[CropFactory],
    in_memory_crop_repo,
    offline_client,
    faker: Faker,
):
    offline_app.dependency_overrides[get_user] = lambda: authenticated_user
    # From other user
    crop: Crop = crop_factory.build()
    n_items = 15
    for crop in crop_factory.build_batch(
        size=n_items,
        owner_id=authenticated_user.id,
    ):
        await in_memory_crop_repo.save(crop=crop)

    response: httpx.Response = offline_client.get(
        url='/v1/crops',
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['items']) == n_items


@pytest.mark.asyncio
async def test_list_crops_with_cursor_ok(
    offline_app,
    authenticated_user: AuthenticatedUser,
    crop_factory: type[CropFactory],
    in_memory_crop_repo,
    offline_client,
    faker: Faker,
):
    offline_app.dependency_overrides[get_user] = lambda: authenticated_user
    n_items = 2
    for crop in crop_factory.build_batch(
        size=n_items,
        owner_id=authenticated_user.id,
    ):
        await in_memory_crop_repo.save(crop=crop)

    first_page_response: httpx.Response = offline_client.get(
        url='/v1/crops',
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
        params={
            # This will return a cursor pointing to the remaining items
            'limit': n_items - 1,
        },
    )
    second_page_response: httpx.Response = offline_client.get(
        url='/v1/crops',
        headers={
            'Authorization': f'Bearer {faker.sha256()}',
        },
        params={
            'limit': 1,
            'cursor': first_page_response.json()['next_cursor'],
        },
    )

    assert second_page_response.status_code == status.HTTP_200_OK
    assert len(second_page_response.json()['items']) == 1
    assert second_page_response.json()['next_cursor'] is None
