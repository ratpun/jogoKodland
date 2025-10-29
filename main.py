import pgzrun
from pygame import Rect

# --- Configuração do Jogo ---
WIDTH = 800
HEIGHT = 600
TITLE = "Jogo Kodland Simplificado"

# --- Constantes ---
GRAVITY = 900
PLAYER_SPEED = 200
PLAYER_JUMP = 450
ENEMY_SPEED = 50

# --- Estado do Jogo ---
game_state = 'menu'
sound_on = True

# --- Atores e Objetos ---
player = Actor('hero/idle_0', anchor=('midbottom', 'bottom'))
enemies = []
platforms = []

# --- Retângulos do Menu ---
start_btn = Rect((WIDTH / 2 - 100, 200), (200, 50))
sound_btn = Rect((WIDTH / 2 - 100, 270), (200, 50))
exit_btn = Rect((WIDTH / 2 - 100, 340), (200, 50))

def setup_game():
    """Configura ou reinicia os elementos do jogo."""
    global platforms, enemies
    player.pos = (WIDTH / 2, HEIGHT - 100)
    player.vy = 0
    player.on_ground = False
    
    platforms = [
        Actor('tiles/platform', pos=(WIDTH / 2, HEIGHT - 20)),
        Actor('tiles/platform', pos=(150, HEIGHT - 150)),
        Actor('tiles/platform', pos=(650, HEIGHT - 150)),
        Actor('tiles/platform', pos=(400, HEIGHT - 300))
    ]
    
    enemies = [Actor('enemy/walk_0', pos=(150, HEIGHT - 182)), Actor('enemy/walk_0', pos=(650, HEIGHT - 182))]
    for i, enemy in enumerate(enemies):
        enemy.patrol_range = 50
        enemy.direction = 1
        enemy.anim_timer = i * 0.1 # Desfasa a animação
    
    if sound_on:
        music.play('background_theme')
        music.set_volume(0.3)

def update_player(dt):
    """Atualiza a lógica e o movimento do jogador."""
    global game_state
    vx = 0
    if keyboard.left:
        vx = -PLAYER_SPEED
        player.scale_x = -1
    elif keyboard.right:
        vx = PLAYER_SPEED
        player.scale_x = 1

    if keyboard.space and player.on_ground:
        player.vy = -PLAYER_JUMP
        if sound_on: sounds.jump.play()

    player.vy += GRAVITY * dt
    player.x += vx * dt
    player.y += player.vy * dt
    player.on_ground = False

    for plat in platforms:
        if player.colliderect(plat) and player.vy >= 0 and player.bottom < plat.top + (player.vy * dt):
            player.bottom = plat.top
            player.vy = 0
            player.on_ground = True
    
    if player.top > HEIGHT: # Checa se caiu
        game_state = 'game_over'
        music.stop()
        if sound_on: sounds.hit.play()

    # Animação do Jogador
    if not player.on_ground: player.image = 'hero/jump'
    elif vx != 0: player.image = 'hero/run_1' if int(player.x / 20) % 2 == 0 else 'hero/run_0'
    else: player.image = 'hero/idle_1' if int(clock.time() * 2) % 2 == 0 else 'hero/idle_0'

def update_enemies(dt):
    """Atualiza a lógica dos inimigos."""
    global game_state
    for enemy in enemies:
        enemy.x += ENEMY_SPEED * enemy.direction * dt
        if abs(enemy.x - enemy.start_pos[0]) > enemy.patrol_range:
            enemy.direction *= -1
            enemy.scale_x = -enemy.direction
        
        # Animação do inimigo
        enemy.image = 'enemy/walk_1' if int(enemy.x / 20) % 2 == 0 else 'enemy/walk_0'

        if player.colliderect(enemy):
            game_state = 'game_over'
            music.stop()
            if sound_on: sounds.hit.play()

def draw():
    """Desenha tudo na tela."""
    screen.clear()
    screen.blit('background', (0, 0))

    if game_state == 'menu':
        screen.draw.text("Aventura na Kodland", center=(WIDTH / 2, 100), fontsize=60, color='white', fontname='kenvector_future_thin')
        for btn, text in [(start_btn, "Iniciar Jogo"), (sound_btn, "Ligar/Desligar Som"), (exit_btn, "Sair")]:
            screen.draw.filled_rect(btn, 'orange')
            screen.draw.textbox(text, btn, color='black', fontname='kenvector_future')

    elif game_state == 'playing':
        for item in platforms + enemies + [player]:
            item.draw()

    elif game_state == 'game_over':
        screen.draw.text("Fim de Jogo!", center=(WIDTH / 2, HEIGHT / 2 - 30), fontsize=80, color='red')
        screen.draw.text("Pressione ENTER para voltar", center=(WIDTH / 2, HEIGHT / 2 + 40), fontsize=30, color='white')

def update(dt):
    """Função de atualização principal, chamada a cada frame."""
    if game_state == 'playing':
        update_player(dt)
        update_enemies(dt)

def on_mouse_down(pos):
    """Lida com cliques do mouse."""
    global game_state, sound_on
    if game_state == 'menu':
        if start_btn.collidepoint(pos):
            game_state = 'playing'
            setup_game()
        elif sound_btn.collidepoint(pos):
            sound_on = not sound_on
        elif exit_btn.collidepoint(pos):
            exit()

def on_key_down(key):
    """Lida com teclas pressionadas."""
    global game_state
    if game_state == 'game_over' and key == keys.RETURN:
        game_state = 'menu'

pgzrun.go()