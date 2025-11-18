from pgzero.builtins import Actor, keyboard, sounds, music

GRAVITY = 900
PLAYER_SPEED = 200
PLAYER_JUMP = 450


class Player:
    def __init__(self, color, pos):
        self.color = color
        self.actor = Actor(f'hero/character_{self.color}_front', anchor=('center', 'bottom'), pos=pos)
        self.reset(pos)

    def reset(self, pos):
        self.actor.pos = pos
        self.direction = 1
        self.vy = 0
        self.on_ground = False
        self.actor.image = f'hero/character_{self.color}_front'

    def update(self, dt, platforms, sound_on, WIDTH, HEIGHT, total_time):
        vx = 0
        if keyboard.left:
            vx = -PLAYER_SPEED
            self.direction = -1
        elif keyboard.right:
            vx = PLAYER_SPEED
            self.direction = 1

        if keyboard.space and self.on_ground:
            self.vy = -PLAYER_JUMP
            if sound_on: sounds.sfx_player_jump.play()

        self.vy += GRAVITY * dt
        self.actor.x += vx * dt
        self.actor.y += self.vy * dt
        self.on_ground = False

        if self.actor.left < 0:
            self.actor.left = 0
        if self.actor.right > WIDTH:
            self.actor.right = WIDTH

        player_feet_center = self.actor.midbottom
        for plat in platforms:
            if plat.collidepoint(player_feet_center) and self.vy >= 0 and self.actor.bottom <= plat.top + 15:
                self.actor.bottom = plat.top
                self.vy = 0
                self.on_ground = True
                break
        
        left_suffix = '_left' if self.direction == -1 else ''
        if not self.on_ground:
            self.actor.image = f'hero/character_{self.color}_jump{left_suffix}'
        elif vx != 0:
            if int(total_time * 10) % 2 == 0:
                self.actor.image = f'hero/character_{self.color}_walk_a{left_suffix}'
            else:
                self.actor.image = f'hero/character_{self.color}_walk_b{left_suffix}'
        else:
            if int(total_time * 2) % 2 == 0:
                self.actor.image = f'hero/character_{self.color}_front{left_suffix}'
            else:
                self.actor.image = f'hero/character_{self.color}_idle{left_suffix}'

        if self.actor.top > HEIGHT:
            music.stop()
            if sound_on: sounds.sfx_player_die.play()
            return 'game_over'

        return 'playing'

    def draw(self):
        self.actor.draw()
