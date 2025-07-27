class Menu:
    def __init__(self):
        self.active = True
        self.sound_enabled = True
        music.play("theme")
        self.button_start = Actor("start", center=(WIDTH // 2, 160))
        self.button_sound = Actor("music_sounds1", center=(WIDTH // 2, 220))
        self.button_exit = Actor("exit", center=(WIDTH // 2, 280))
        self.background = Background("background_color_trees", y=0, scroll_speed=0)

    def draw(self):
        self.background.draw()
        self.button_start.draw()
        self.button_sound.draw()
        self.button_exit.draw()
        screen.draw.text(f"Jumping Adventure", center=(WIDTH // 2, 70), fontsize=40, color="white", owidth=1.0, ocolor="black")

    def on_mouse_down(self, pos):
        if self.button_start.collidepoint(pos):
            self.active = False 
        elif self.button_sound.collidepoint(pos):
            self.sound_enabled = not self.sound_enabled
            if menu.sound_enabled:
                music.play("theme")
            elif not menu.sound_enabled:
                music.stop()
            self.button_sound.image = "music_sounds1" if self.sound_enabled else "music_sounds2"
        elif self.button_exit.collidepoint(pos):
            exit()


    def reset_game(self):
        global score, player, enemy
        score = 0
        player.lives = 3
        player.actor.pos = (100, 200)
        player.velocity_y = 0
        enemy.actor.pos = (500, 283)
        enemy.speed = 2

class Player:
    def __init__(self, x, y):
        self.images_walk = ['p_walk1', 'p_walk2', 'p_walk3']
        self.images_idle = ['p_idle1', 'p_idle2']
        self.sprite_index = 0
        self.frame_counter = 0
        self.actor = Actor(self.images_idle[0], (x, y))
        self.velocity_y = 0
        self.ground = False
        self.walking = False
        self.idle_animating = True
        self.lives = 3
        self.damage_cooldown = False

    def update(self, keyboard):
        speed = 8
        self.walking = False

        if keyboard.left:
            self.actor.x -= speed
            self.walking = True
        if keyboard.right:
            self.actor.x += speed
            self.walking = True

        if keyboard.space and self.ground:
            self.velocity_y = -17
            self.ground = False
            

        self.velocity_y += 1
        self.actor.y += self.velocity_y

        floor = 259
        if self.actor.y > floor:
            self.actor.y = floor
            self.velocity_y = 0
            self.ground = True
        else:
            self.ground = False

        if self.actor.left < 0:
            self.actor.left = 0
        if self.actor.right > WIDTH:
            self.actor.right = WIDTH
        self.animate()


    def animate(self):
        self.frame_counter += 1

        if not self.ground and self.velocity_y < 0:
            self.actor.image = 'p_jump'

        elif self.walking:
            if self.frame_counter % 10 == 0:
                self.sprite_index = (self.sprite_index + 1) % len(self.images_walk)
                self.actor.image = self.images_walk[self.sprite_index]

        else:
            if self.frame_counter % 30 == 0:
                self.sprite_index = (self.sprite_index + 1) % len(self.images_idle)
                self.actor.image = self.images_idle[self.sprite_index]
    
    def set_player_normal(self):
        self.actor.image = 'p_idle1'

    def set_player_hit(self):
        self.actor.image = 'p_hit'
        clock.schedule_unique(self.set_player_normal, 1.0)
        if menu.sound_enabled:
            sounds.hit.play()

    def draw(self):
        self.actor.draw()

    def damage(self, enemy):
        if enemy.collides_with(self.actor) and self.lives > 0 and not self.damage_cooldown:
            self.lives -= 1
            self.set_player_hit()
            self.damage_cooldown = True
class Background:
    def __init__(self, image_name, y=0, scroll_speed=4):
        self.image_name = image_name
        self.y = y
        self.scroll_speed = scroll_speed

        self.width = 512
        self.image_left_x = 0
        self.image_right_x = self.width

    def update(self):
        self.image_left_x -= self.scroll_speed
        self.image_right_x -= self.scroll_speed

        if self.image_left_x + self.width <= 0:
            self.image_left_x = self.image_right_x + self.width
        if self.image_right_x + self.width <= 0:
            self.image_right_x = self.image_left_x + self.width
            

    def draw(self):
        screen.blit(self.image_name, (self.image_left_x, self.y))
        screen.blit(self.image_name, (self.image_right_x, self.y))
class Platform:
    def __init__(self, x, y):
        self.actor = Actor('platform', (x, y))

    def update(self, speed):
        self.actor.x -= speed
        if self.actor.right < 0:
            self.actor.left = WIDTH
          

    def draw(self):
        self.actor.draw()
class Enemy:
    def __init__(self, x, y, speed=2):
        self.actor = Actor("snail_rest", (x, y))
        self.speed = speed
        self.sprite_index = 0
        self.frame_count = 0
        self.walk_images = ["snail_walk_a", "snail_walk_b", ]

    def update(self):
        self.actor.x -= self.speed

        
        if self.actor.right < 0:
            self.actor.left = WIDTH + 50
            self.speed += 0.25

        self.frame_count += 1
        if self.frame_count % 10 == 0:
            self.sprite_index = (self.sprite_index + 1) % len(self.walk_images)
            self.actor.image = self.walk_images[self.sprite_index]

    def draw(self):
        self.actor.draw()

    def collides_with(self, other_actor):
        return self.actor.colliderect(other_actor)


WIDTH = 512
HEIGHT = 400

sound_enabled = True
menu = Menu()

button_start = Actor("start", center=(WIDTH // 2, 160))
button_sound = Actor("start", center=(WIDTH // 2, 220))
button_exit = Actor("exit", center=(WIDTH // 2, 280))

background_hills = Background("background_color_hills", y=0, scroll_speed=1)
background_ground = Background("terrain", y=300, scroll_speed=3)
platform = Platform(300, 210)


player = Player(100, 200)
enemy = Enemy(500, 283)
score = 0
frame_counter = 0
game_over = False
playerDamage_cooldown = False
playerDamage_cooldownFrames = 0


def update():
    global score, frame_counter, game_over, playerDamageCooldown, playerDamage_cooldownFrames
    
    if menu.active:
        return


    if player.damage_cooldown:
        playerDamage_cooldownFrames += 1
        if playerDamage_cooldownFrames >= 90:
            player.damage_cooldown = False
            playerDamage_cooldownFrames = 0

    if player.ground or player.actor.bottom >= platform.actor.top:
        player.actor.x -= 3 

    if player.actor.colliderect(platform.actor):
        if player.velocity_y > 0 and player.actor.bottom <= platform.actor.top + 10:
            player.actor.bottom = platform.actor.top 
            player.velocity_y = 0
            player.ground = True
            
    frame_counter += 1
    if frame_counter >= 40:
        score += 1
        frame_counter = 0

    player.update(keyboard)
    background_hills.update()
    background_ground.update()
    platform.update(3)

    enemy.update()
    player.damage(enemy)


    if player.lives <= 0:
        menu.active = True
        menu.reset_game()


def draw():
    screen.clear()
    
    if menu.active:
        menu.draw()
    else:
        background_hills.draw()
        background_ground.draw()
        platform.draw()
        screen.draw.text(f"Score: {score}", center=(WIDTH // 2, 30), fontsize=30, color="white", owidth=1.0, ocolor="black")

        player.draw()
        for i in range (player.lives):
            screen.blit("hud_heart", (10 + i * 40, 10))
        
        enemy.draw()

def on_mouse_down(pos):
    if menu.active:
        menu.on_mouse_down(pos)