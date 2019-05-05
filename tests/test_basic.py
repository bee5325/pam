import pytest
from pam.actor import Actor, Act
from pam.scene import Scene


# ---------------------------------- ACTOR ---------------------------------- #
@pytest.fixture()
def empty_actor():
    return Actor()


@pytest.fixture()
def normal_actor():
    a = Actor()
    a.add_action(Act.MOVE, 1, (100, 100))
    a.add_action(Act.ROTATE, 2, 90)
    a.add_action(Act.MOVE, 0.5, (200, 200))
    return a


@pytest.fixture()
def busy_actor():
    actor = Actor()
    actor.add_action(Act.STOP, 2)
    actor.add_action(Act.MOVE, 2, (100, 100))
    actor.add_action(Act.ROTATE, 2, 90)
    return actor


def test_actor_init(empty_actor):
    assert empty_actor.actions_count() == 1


def test_actor_add_action(empty_actor):
    empty_actor.add_action(Act.STOP, 2)
    empty_actor.add_action(Act.MOVE, 1, (100, 100))
    empty_actor.add_action(Act.ROTATE, 1, 90)

    assert empty_actor.actions_count() == 4
    assert empty_actor.actions[0].type == Act.STOP
    assert empty_actor.actions[0].duration == 2
    assert empty_actor.actions[0].dest == ""
    assert empty_actor.actions[1].type == Act.MOVE
    assert empty_actor.actions[1].duration == 1
    assert empty_actor.actions[1].dest == (100, 100)
    assert empty_actor.actions[2].type == Act.ROTATE
    assert empty_actor.actions[2].duration == 1
    assert empty_actor.actions[2].dest == 90
    assert empty_actor.actions[3].type == Act.STOP
    assert empty_actor.actions[3].duration == 0
    assert empty_actor.actions[3].dest == ""


def test_actor_action_at(normal_actor):
    assert normal_actor.action_at(0).type == Act.MOVE
    assert normal_actor.action_at(0.5).type == Act.MOVE
    assert normal_actor.action_at(1).type == Act.ROTATE
    assert normal_actor.action_at(1.5).type == Act.ROTATE
    assert normal_actor.action_at(2).type == Act.ROTATE
    assert normal_actor.action_at(2.5).type == Act.ROTATE
    assert normal_actor.action_at(3).type == Act.MOVE
    assert normal_actor.action_at(3.5).type == Act.STOP
    assert normal_actor.action_at(4).type == Act.STOP


def test_actor_move(busy_actor):
    # check if the configuration is correct
    assert busy_actor.action_at(2).type == Act.MOVE
    assert busy_actor.action_at(2).dest == (100, 100)

    # check if position changes with time
    assert busy_actor.position == (0, 0)


# ---------------------------------- SCENE ---------------------------------- #
@pytest.fixture()
def basic_scene():
    return Scene()


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







