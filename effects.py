from pgzero.builtins import Actor


class ExplosionAnimation:
    def __init__(self, pos):
        self.frames = [f'effects/projectile_explosion_-{i}' for i in range(1, 6)]
        self.actor = Actor(self.frames[0], pos=pos)

        self.anim_timer = 0.0
        self.anim_frame_duration = 0.08
        self.current_frame = 0
        self.finished = False

    def update(self, dt):
        if self.finished:
            return

        self.anim_timer += dt
        if self.anim_timer >= self.anim_frame_duration:
            self.anim_timer = 0.0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True
            else:
                self.actor.image = self.frames[self.current_frame]

    def draw(self):
        if not self.finished:
            self.actor.draw()