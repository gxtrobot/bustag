import pytest


@pytest.fixture(scope="session", autouse=True)
def start():
    print("\n **** start test ****")
