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

        if keyboard.left:
            self.actor.x -= speed
            self.walking = True
        if keyboard.right:
            self.actor.x += speed
            self.walking = True

        if keyboard.space and self.ground:
            self.velocity_y = -15
            self.ground = False

        self.velocity_y += 1
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


WIDTH = 512
HEIGHT = 400

background_hills = Background("background_color_hills", y=0, scroll_speed=1)
background_ground = Background("terrain", y=300, scroll_speed=3)


player = Player(100, 200)
def update():
    player.update(keyboard)
    background_hills.update()
    background_ground.update()

def draw():
    screen.clear()
    background_hills.draw()
    background_ground.draw()
    player.draw()