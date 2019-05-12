import pytest

from pygame import Rect

from pam.actor import Actor
from pam.action import ActMove, ActRotate, ActStop, Action
from pam.scene import Scene


# ---------------------------------- ACTOR ---------------------------------- #
@pytest.fixture()
def empty_actor():
    return Actor()


@pytest.fixture()
def normal_actor():
    a = Actor()
    a.add_action(ActMove, 1, (100, 200))
    a.add_action(ActRotate, 2, 90)
    a.add_action(ActMove, 0.5, (200, 100))
    return a


@pytest.fixture()
def busy_actor():
    actor = Actor()
    actor.add_action(ActStop, 2)
    actor.add_action(ActMove, 2, (100, 200))
    actor.add_action(ActRotate, 2, 90)
    return actor


def test_actor_init(empty_actor):
    assert empty_actor.actions_count() == 1
    assert empty_actor.rect.topleft == (0, 0)
    assert empty_actor.rect.width == 0
    assert empty_actor.rect.height == 0


def test_actor_change_size(empty_actor):
    empty_actor.rect = (1, 2, 10, 20)
    assert empty_actor.rect.left == 1
    assert empty_actor.rect.top == 2
    assert empty_actor.rect.width == 10
    assert empty_actor.rect.height == 20
    assert empty_actor.image.get_width() == 10
    assert empty_actor.image.get_height() == 20


def test_actor_add_action(empty_actor):
    empty_actor.add_action(ActStop, 2)
    empty_actor.add_action(ActMove, 1, (100, 200))
    empty_actor.add_action(ActRotate, 1, 90)

    assert empty_actor.actions_count() == 4
    assert empty_actor.actions[0].type == "ActStop"
    assert empty_actor.actions[0].duration == 2
    assert empty_actor.actions[0].dest == ""
    assert empty_actor.actions[1].type == "ActMove"
    assert empty_actor.actions[1].duration == 1
    assert empty_actor.actions[1].dest == (100, 200)
    assert empty_actor.actions[2].type == "ActRotate"
    assert empty_actor.actions[2].duration == 1
    assert empty_actor.actions[2].dest == 90
    assert empty_actor.actions[3].type == "ActStop"
    assert empty_actor.actions[3].duration == 0
    assert empty_actor.actions[3].dest == ""


def test_actor_action_at(normal_actor):
    assert normal_actor.action_at(0).type == "ActMove"
    assert normal_actor.action_at(0.5).type == "ActMove"
    assert normal_actor.action_at(1).type == "ActRotate"
    assert normal_actor.action_at(1.5).type == "ActRotate"
    assert normal_actor.action_at(2).type == "ActRotate"
    assert normal_actor.action_at(2.5).type == "ActRotate"
    assert normal_actor.action_at(3).type == "ActMove"
    assert normal_actor.action_at(3.5).type == "ActStop"
    assert normal_actor.action_at(4).type == "ActStop"


def test_actor_move(empty_actor):

    empty_actor.add_action(ActMove, 2, (100, 200))

    # check if position changes with time
    assert empty_actor.position == (0, 0)
    empty_actor.update(0.0167)
    assert empty_actor.position == (0.835, 1.67)
    empty_actor.update(1)
    assert empty_actor.position == (50, 100)
    empty_actor.update(2)
    assert empty_actor.action_at(2).type == "ActStop"
    assert empty_actor.state_at(2)["position"] == (100, 200)
    assert empty_actor.position == (100, 200)
    empty_actor.update(3)
    assert empty_actor.position == (100, 200)


def test_actor_stop(empty_actor):

    assert empty_actor.state_at(0) == empty_actor.state_at(100)
    

def test_actor_add_action_type(empty_actor):

    class ActCustom(Action):

        def state_after(self, time_passed):
            return dict(self.start_state, custom_state=time_passed)

    empty_actor.add_action(ActCustom, 2, 0)
    assert empty_actor.action_at(0).type == "ActCustom"
    assert empty_actor.state_at(0)["custom_state"] == 0
    assert empty_actor.state_at(1)["custom_state"] == 1

    assert empty_actor.action_at(3).type == "ActStop"
    assert empty_actor.state_at(3)["custom_state"] == 2


# ---------------------------------- SCENE ---------------------------------- #
@pytest.fixture()
def basic_scene():
    return Scene(600, 400)


def test_scene_init():
    new_scene = Scene(600, 400)
    assert new_scene.width == 600
    assert new_scene.height == 400
    assert type(new_scene.screen).__name__ == "Surface"


def test_scene_running(basic_scene):
    basic_scene.set_framerate(60)

    assert basic_scene.time == 0
    basic_scene.update()
    assert basic_scene.time == 0.0167
    basic_scene.update()
    assert basic_scene.time == 0.0334
    basic_scene.update()
    assert basic_scene.time == 0.0501


def test_scene_update_actor(basic_scene, busy_actor):
    basic_scene.add_actor(busy_actor)
    basic_scene.set_framerate(60)

    assert busy_actor.time == 0
    basic_scene.update()
    assert busy_actor.time == 0.0167
    basic_scene.update()
    assert busy_actor.time == 0.0334
    basic_scene.update()
    assert busy_actor.time == 0.0501
