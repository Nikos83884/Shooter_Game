from pygame import *
from random import randint  

window = display.set_mode((700, 500))
background = transform.scale(image.load("galaxy.jpg"), (700, 500)) 

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):  
        super().__init__()
        self.image = transform.scale(image.load(player_image), (55, 55))
        self.speed = player_speed
        self.rect = self.image.get_rect() 
        self.rect.x = player_x
        self.rect.y = player_y
        
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y)) 

bullets = sprite.Group()

#Create the rocket object with its movement
class Rocket(GameSprite):
    def movement(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < (700-55):
            self.rect.x += self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
    
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.x, 445, 5)
        bullets.add(bullet)


#Creates the Ufo object with its movement
class Ufo(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y >= 480:
            self.rect.y = 0
            self.rect.x = randint(0, (700-55))
            self.speed = randint(1, 5)
            missed += 1

#Create the bullet object with its movement
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed


rocket = Rocket("rocket.png", 12, 445, 10)
ufos = sprite.Group()
for i in range(5):
    ufo = Ufo("ufo.png", randint(0, 650), 0, randint(1, 4))
    ufos.add(ufo)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.1)
mixer.music.play()

font.init()
font1 = font.SysFont(None, 50)
font2 = font.SysFont(None ,30)


clock = time.Clock()
FPS = 60

#Create the needed variables for the victory, defeat, missed counter, score counter, 
lose = font1.render("You lost!", True, (255, 0 ,0))
victory = font1.render("You won!", True, (255, 0, 0))
score = 0
missed = 0
finish = False
game = True

font.init()
font2 = font.Font(None, 36)

while game:
    window.blit(background, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
            elif e.key == K_r and finish:  # Check for 'R' key press when game is finished
                # Reset game state
                score = 0
                missed = 0
                finish = False
                ufos.empty()  # Remove existing UFOs
                for i in range(5):  # Create new UFOs
                    ufo = Ufo("ufo.png", randint(0, 650), 0, randint(1, 4))
                    ufos.add(ufo)
                mixer.music.set_volume(0.1) # Restore music to its original volume  

    # Draw game elements
    rocket.draw()
    ufos.draw(window)
    bullets.draw(window)

    # Handle collisions and score updates
    collide = sprite.groupcollide(ufos, bullets, True, True)
    for i in collide:
        score += 1
        ufo = Ufo("ufo.png", randint(0, 650), 0, randint(1, 3))
        ufos.add(ufo)

    # Check for game over conditions
    if sprite.spritecollide(rocket, ufos, True) or missed >= 5:
        window.blit(lose, (200, 200))
        finish = True
        mixer.music.set_volume(0)
        
    # Check for victory condition
    if score >= 5:
        window.blit(victory, (200, 200))
        finish = True
        mixer.music.set_volume(0)

    # Display score and missed count
    text1 = font2.render(f"Score: {score}", 1, (255, 255, 255))
    window.blit(text1, (10, 20))

    text2 = font2.render(f"Missed: {missed}", 1, (255, 255, 255)) 
    window.blit(text2, (10, 45))

    #Update game elements if the game is not finished
    if finish == False:
        bullets.update()
        ufos.update()
        rocket.movement()

    clock.tick(FPS)
    display.update()