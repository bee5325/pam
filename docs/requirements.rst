Requirements
============

Scenes
------
1. Time flow is controlled through realtime clock, not frame
2. Multiple scenes can be joined together to form a complete movie
3. Every dynamic object in the scene should be actor
4. Controlling the render sequence of the actors

Actors
------
1. Should have enough information to decide how it should behave at any time
   given in the movie

Actions
-------
1. Basic Actions:
    a. Stop
    b. Move
    c. Rotate
    d. Animation
    e. Changing attributes: Eg color, size
2. Each action should has:
    a. Start time
    b. Duration
    c. Starting point (depends on action type)
    d. Ending point (depends on action type)

Editor
------
1. Able to start / pause the playing scene anytime
2. Able to control the playing speed in between +/- 0.5x-4x
3. Able to insert extra actors into the scene
4. Extra actors can:
    a. Having basic actions - see Actions_
    b. Follow another actor
5. Able to set keyframes in the movie
6. Smallest time scale - 1/60s = 0.0167s

Movie
-----
1. Able to start / pause the playing scene anytime
2. Able to control the playing speed in between +/- 0.5x-4x
3. Able to automatically pause at keyframes
4. Smallest time scale - 1/60s = 0.0167s

Output from editor
------------------
1. Input and output can be modified independently
