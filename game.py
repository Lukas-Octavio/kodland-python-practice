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

    def update(self, keyboard):
        speed = 2
        self.walking = False

        # Movimento
        if keyboard.left:
            self.actor.x -= speed
            self.walking = True
        if keyboard.right:
            self.actor.x += speed
            self.walking = True

        # Pulo
        if keyboard.space and self.ground:
            self.velocity_y = -15
            self.ground = False

        # Gravidade
        self.velocity_y += 1  # força da gravidade
        self.actor.y += self.velocity_y

        floor = 245
        if self.actor.y > floor:
            self.actor.y = floor
            self.velocity_y = 0
            self.ground = True
        else:
            self.ground = False

        self.animate()


    def animate(self):
        self.frame_counter += 1

        if not self.ground:
            self.actor.image = 'p_jump'

        elif self.walking:
            if self.frame_counter % 10 == 0:
                self.sprite_index = (self.sprite_index + 1) % len(self.images_walk)
                self.actor.image = self.images_walk[self.sprite_index]

        else:
            if self.frame_counter % 30 == 0:
                self.sprite_index = (self.sprite_index + 1) % len(self.images_idle)
                self.actor.image = self.images_idle[self.sprite_index]

    def draw(self):
        self.actor.draw()




WIDTH = 512
HEIGHT = 400

player = Player(100, 200)
def update():
    player.update(keyboard)

def draw():
    screen.clear()
    # desenhar cenário, plataformas, etc.
    player.draw()