import pgzrun
from pygame import Rect
import random
from player import Player
from enemy import Enemy
from effects import ExplosionAnimation

WIDTH = 800
HEIGHT = 600
TITLE = "Space Exploders"

game_state = 'menu'
sound_on = True
selected_level = 'hills'
total_time = 0
game_timer = 0

player = Player('purple', (WIDTH / 2, HEIGHT - 100))
enemies = []
platforms = []
effects_animations = []

start_btn = Rect((WIDTH / 2 - 100, 250), (200, 50))
sound_btn = Rect((WIDTH / 2 - 100, 320), (200, 50))
exit_btn = Rect((WIDTH / 2 - 100, 390), (200, 50))

sound_icon_on = Actor('ui/megaphone_on')
sound_icon_off = Actor('ui/megaphone_off')

music.play('menu_music')
music.set_volume(0.3)
if not sound_on:
    music.pause()


def setup_game():
    global platforms, enemies, effects_animations, game_timer

    player.reset((WIDTH / 2, HEIGHT - 100))
    game_timer = 0

    platforms = []
    enemies = []
    effects_animations = []

    try:
        ground_tile = Actor('tiles/terrain_grass_block_top')
        cloud_tile = Actor('tiles/terrain_stone_cloud')
        ground_tile_width, ground_tile_height = ground_tile.width, ground_tile.height
        cloud_tile_width, cloud_tile_height = cloud_tile.width, cloud_tile.height
    except Exception:
        ground_tile_width, ground_tile_height = 70, 70
        cloud_tile_width, cloud_tile_height = 70, 70

    num_tiles_ground = (WIDTH // ground_tile_width) + 1
    for i in range(num_tiles_ground):
        x_pos = i * ground_tile_width
        platforms.append(Actor('tiles/terrain_grass_block_top', bottomleft=(x_pos, HEIGHT)))

    num_platforms = random.randint(7, 10)
    spawn_points = []
    platform_rects = [Rect(0, HEIGHT - ground_tile_height, WIDTH, ground_tile_height)]
    last_y = HEIGHT - ground_tile_height
    last_x_center = WIDTH / 2
    MAX_JUMP_HEIGHT, MIN_VERTICAL_GAP = 100, 40

    for _ in range(num_platforms):
        length = random.randint(3, 5)
        plat_width = length * cloud_tile_width
        retry_count = 0
        while retry_count < 15:
            x_offset = random.randint(-WIDTH // 4, WIDTH // 4)
            y_offset = random.randint(MIN_VERTICAL_GAP, int(MAX_JUMP_HEIGHT))
            start_x = last_x_center + x_offset - (plat_width / 2)
            start_y = last_y - y_offset
            start_x = max(0, min(start_x, WIDTH - plat_width))
            start_y = max(100, min(start_y, HEIGHT - 150))
            new_plat_rect = Rect(start_x, start_y, plat_width, cloud_tile_height)
            if not any(new_plat_rect.colliderect(r.inflate(cloud_tile_width, cloud_tile_height)) for r in platform_rects):
                platform_spawn_points = []
                for i in range(length):
                    tile_x = start_x + i * cloud_tile_width
                    platforms.append(Actor('tiles/terrain_stone_cloud', topleft=(tile_x, start_y)))
                    if 0 < i < length - 1:
                        platform_spawn_points.append((tile_x + cloud_tile_width / 2, start_y))

                if platform_spawn_points:
                    spawn_points.append(
                        (random.choice(platform_spawn_points), (new_plat_rect.left, new_plat_rect.right))
                    )

                platform_rects.append(new_plat_rect)
                last_y, last_x_center = start_y, new_plat_rect.centerx
                break
            retry_count += 1

    num_enemies = random.randint(2, 4)
    enemy_types = ['normal', 'fire', 'spike']
    chosen_spawns = random.sample(spawn_points, min(num_enemies, len(spawn_points)))
    for i, (pos, patrol_bounds) in enumerate(chosen_spawns):
        enemy_type = random.choice(enemy_types)
        enemies.append(Enemy(enemy_type, pos, patrol_bounds, anim_offset=i * 0.1))

    music.play('game_music')
    music.set_volume(0.3)
    if not sound_on:
        music.pause()


def check_player_enemy_collisions():
    enemies_to_remove = []
    
    player_hitbox = Rect(
        player.actor.centerx - (player.actor.width * 0.4) / 2,
        player.actor.bottom - (player.actor.height * 0.7),
        player.actor.width * 0.4,
        player.actor.height * 0.7
    )

    for enemy in enemies:
        if enemy in enemies_to_remove:
            continue
            
        enemy_hitbox = Rect(
            enemy.actor.centerx - (enemy.actor.width * 0.6) / 2,
            enemy.actor.bottom - (enemy.actor.height * 0.5),
            enemy.actor.width * 0.6,
            enemy.actor.height * 0.5
        )
        if player_hitbox.colliderect(enemy_hitbox):
            enemies_to_remove.append(enemy)
            effects_animations.append(ExplosionAnimation(enemy.actor.pos))
            if sound_on: sounds.sfx_enemy_die.play()

    for enemy in enemies_to_remove:
        if enemy in enemies:
            enemies.remove(enemy)


def draw():
    screen.clear()

    if game_state == 'menu':
        screen.fill('saddlebrown')
        
        screen.draw.text("Space Exploders", center=(WIDTH / 2, 150), fontsize=60, color='white')
        for btn, text in [(start_btn, "Iniciar Jogo"), (sound_btn, "Ligar/Desligar Som"), (exit_btn, "Sair")]:
            screen.draw.filled_rect(btn, 'orange')
            screen.draw.textbox(text, btn, color='black')
        
        active_sound_icon = sound_icon_on if sound_on else sound_icon_off
        active_sound_icon.midleft = (sound_btn.right + 10, sound_btn.centery)
        active_sound_icon.draw()

    elif game_state in ['playing', 'game_over', 'victory']:
        try:
            bg_image_name = f'backgrounds/background_color_{selected_level}.png'
            bg_clouds_name = 'backgrounds/background_clouds.png'
            temp_bg = Actor(bg_image_name)
            temp_clouds = Actor(bg_clouds_name)
            bg_width, bg_height = temp_bg.width, temp_bg.height
            clouds_width, clouds_height = temp_clouds.width, temp_clouds.height
            for y in range(0, HEIGHT, bg_height):
                for x in range(0, WIDTH, bg_width):
                    screen.blit(bg_image_name, (x, y))
            for y in range(0, HEIGHT, clouds_height):
                for x in range(0, WIDTH, clouds_width):
                    screen.blit(bg_clouds_name, (x, y))
        except Exception:
            screen.fill('black')

        for p in platforms: p.draw()
        for e in enemies: e.draw()
        for anim in effects_animations: anim.draw()
        player.draw()

        timer_text = f"Tempo: {game_timer:.2f}"
        screen.draw.text(timer_text, topright=(WIDTH - 15, 15), fontsize=30, color='white', ocolor='black', owidth=1)

    if game_state == 'game_over':
        screen.draw.text("Fim de Jogo!", center=(WIDTH / 2, HEIGHT / 2 - 30), fontsize=80, color='red', owidth=1.5,
                        ocolor="black")
        screen.draw.text("Pressione ENTER para tentar novamente", center=(WIDTH / 2, HEIGHT / 2 + 40), fontsize=30,
                        color='white', owidth=1, ocolor="black")

    if game_state == 'victory':
        screen.draw.text("Você Venceu!", center=(WIDTH / 2, HEIGHT / 2 - 50), fontsize=80, color='yellow', owidth=1.5, ocolor="black")
        final_time_text = f"Seu tempo: {game_timer:.2f}s"
        screen.draw.text(final_time_text, center=(WIDTH / 2, HEIGHT / 2 + 20), fontsize=40, color='white', owidth=1, ocolor="black")
        screen.draw.text("Pressione ENTER para a próxima fase", center=(WIDTH / 2, HEIGHT / 2 + 70), fontsize=30, color='white', owidth=1, ocolor="black")


def update(dt):
    global total_time, game_state, game_timer

    total_time += dt

    if game_state == 'playing':
        game_timer += dt

        new_state = player.update(dt, platforms, sound_on, WIDTH, HEIGHT, total_time)
        if new_state != game_state:
            game_state = new_state
            return

        for enemy in enemies:
            enemy.update(dt, total_time)
        
        for anim in effects_animations[:]:
            anim.update(dt)
            if anim.finished:
                effects_animations.remove(anim)

        check_player_enemy_collisions()

        if not enemies:
            game_state = 'victory'
            music.stop()


def on_mouse_down(pos):
    global game_state, sound_on
    if game_state == 'menu':
        if start_btn.collidepoint(pos):
            if sound_on: sounds.sfx_button_select.play()
            game_state = 'playing'
            setup_game()
        elif sound_btn.collidepoint(pos):
            if sound_on: sounds.sfx_button_select.play()
            sound_on = not sound_on
            if sound_on:
                music.unpause()
            else:
                music.pause()
        elif exit_btn.collidepoint(pos):
            if sound_on: sounds.sfx_button_select.play()
            exit()


def on_key_down(key):
    global game_state
    if (game_state == 'game_over' or game_state == 'victory') and key == keys.RETURN:
        setup_game()
        game_state = 'playing'


pgzrun.go()