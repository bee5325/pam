"use strict";

var actorsjson = '['+ 
'{"position":[50,50], "width":20, "height":40,'+
'  "actions": ['+
'    { "type":"move", "duration": 20,'+
'      "start": { "position": [50,50], "color":[255,255,255] },'+
'      "end":   { "position": [50,300], "color":[255,255,255] }'+
'    }'+
'  ]'+
'}'+
']'
var scene;
var t = 0;


function setup() {
  createCanvas(640, 480);
  let jsonactors = JSON.parse(actorsjson);
  let myActors = [];
  for (const actor of jsonactors) {
    myActors.push(Object.assign(Actor, actor));
  }
  scene = { endTime: 10, actors: myActors };
}

function draw() {
  background(0);
  update(scene);
  t += 0.1;
}


// ----------------------------------------------------------------------

let running = true;
let lastTimer = millis();
let time = 0;

function update(scene) {
  if (running) {
    time += (millis()-lastTimer) / 1000;
    time = min(scene.endTime, time)
    console.log(scene.actors);
    for (const actor of scene.actors) {
      actor.update(time);
    }
    lastTimer = millis();
  }
}


// ----------------------------------------------------------------------

const Actor = {
  update: function(time) { console.log("Updating"); }
}



/*
  const {duration, start, end} = actor.actions[0];
  let timeRatio = time / duration;
  let posX = map(timeRatio, 0, duration, start.position[0], end.position[0]);
  let posY = map(timeRatio, 0, duration, start.position[1], end.position[1]);
  rect(posX, posY, actor.width, actor.height);
}


    def update(self):
        if self.running:
            # control framerate
            timediff = (pygame.time.get_ticks() - self._last_timer) / 1000
            if timediff < self._timestep:
                pygame.time.delay(int((self._timestep-timediff)*1000))

            if self._direction == PlayDir.FORWARD:
                self._time += (pygame.time.get_ticks()-self._last_timer) / 1000
                self._time = min(self.end_time, self._time)
            elif self._direction == PlayDir.BACKWARD:
                self._time -= (pygame.time.get_ticks()-self._last_timer) / 1000
                self._time = max(0, self._time)
            for group in self.groups.values():
                group.update(self._time)
            self._last_timer = pygame.time.get_ticks()
*/
