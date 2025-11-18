from pgzero.builtins import Actor

ENEMY_SPEED = 50


class Enemy:
    def __init__(self, type, pos, patrol_bounds, anim_offset=0.0):
        self.type = type
        self.actor = Actor(f"enemy/slime_{self.type}_walk_a", midbottom=pos)
        self.patrol_left = patrol_bounds[0]
        self.patrol_right = patrol_bounds[1]
        self.direction = 1
        self.anim_timer_offset = anim_offset
        self.actor.image = f"enemy/slime_{self.type}_walk_a_left"

    def update(self, dt, total_time):
        self.actor.x += ENEMY_SPEED * self.direction * dt

        if self.direction == 1 and self.actor.right > self.patrol_right:
            self.direction = -1
            self.actor.right = self.patrol_right
        elif self.direction == -1 and self.actor.left < self.patrol_left:
            self.direction = 1
            self.actor.left = self.patrol_left

        left_suffix = '_left' if self.direction == 1 else ''
        if int((total_time + self.anim_timer_offset) * 5) % 2 == 0:
            self.actor.image = f'enemy/slime_{self.type}_walk_b{left_suffix}'
        else:
            self.actor.image = f'enemy/slime_{self.type}_walk_a{left_suffix}'

    def draw(self):
        self.actor.draw()