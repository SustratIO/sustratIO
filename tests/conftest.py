import logging
import pathlib
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from domain.ports.repositories.crop_repository import CropRepositoryPort

logger = logging.getLogger(__name__)

# The root folder of the project, used for locating test data and other
# resources.
root_folder = pathlib.Path(__file__).parent.parent

# Add the 'src' directory to the Python path if it exists, allowing tests to
# import modules from there.
if (root_folder / 'src').exists():
    import sys

    sys.path.append(str(root_folder / 'src'))


from pytest_factoryboy import register
from tests.factories.auth_factory import AuthenticatedUserFactory

register(AuthenticatedUserFactory)

from tests.factories.crop_factory import CropFactory

register(CropFactory)


@pytest.fixture
def in_memory_crop_repo() -> CropRepositoryPort:
    """
    Returns an implementation of in-memory crop repository.
    """

    from infrastructure.adapters.persistence.in_memory.crop_repository import (
        InMemoryCropRepository,
    )

    return InMemoryCropRepository()
