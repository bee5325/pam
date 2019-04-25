import pytest
from sandbox import actor

@pytest.fixture()
def empty_actor():
    return actor.Actor()

def test_actor_init(empty_actor):
    assert len(empty_actor.actions) == 0
