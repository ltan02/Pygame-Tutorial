import pygame

pygame.init() #initialise pygame

WIN = pygame.display.set_mode((500, 480)) #Creates the actual window
pygame.display.set_caption("First Game") #Caption for the window

screenWidth = 500
screenHeight = 480

#loading images to python
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

#clockspeed
clock = pygame.time.Clock()

class Player(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = 5
		self.isJump = False
		self.jumpCount = 10
		self.left = False
		self.right = False
		self.walkCount = 0
		self.standing = True
		self.hitbox = (self.x + 17, self.y + 11, 29, 52) #x, y, width, height

	def draw(self, win):
		if self.walkCount + 1 >= 27:
			self.walkCount = 0

		if not(self.standing):
			if self.left:
				win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
			elif self.right:
				win.blit(walkRight[self.walkCount//3], (self.x, self.y))
				self.walkCount += 1
		else:
			if self.right:
				win.blit(walkRight[0], (self.x, self.y))
			else:
				win.blit(walkLeft[0], (self.x, self.y))
		self.hitbox = (self.x + 17, self.y + 11, 29, 52)
		pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) #drawing the hitbox

class Projectile(object):
	def __init__(self, x, y, radius, color, facing):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.facing = facing
		self.vel = 8 * facing

	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Enemy(object):
	walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
	walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

	def __init__(self, x, y, width, height, end):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.end = end
		self.path = [self.x, self.end]
		self.walkCount = 0
		self.vel = 3
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)

	def draw(self, win):
		self.move()
		if self.walkCount + 1 >= 33:
			self.walkCount = 0

		if self.vel > 0:
			win.blit(self.walkRight[self.walkCount//3], (self.x, self.y))
			self.walkCount += 1
		else:
			win.blit(self.walkLeft[self.walkCount//3], (self.x, self.y))
			self.walkCount += 1
		self.hitbox = (self.x + 17, self.y + 2, 31, 57)
		pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

	def move(self):
		if self.vel > 0:
			if self.x + self.vel < self.path[1]:
				self.x += self.vel
			else:
				self.vel *= -1
				self.walkCount = 0
		else:
			if self.x - self.vel > self.path[0]:
				self.x += self.vel
			else:
				self.vel *= -1
				self.walkCount = 0

	def hit(self):
		print("HIT")

def redrawGameWindow(): #drawing occurs in this function
	WIN.blit(bg, (0,0)) #fill the screen with a picture
	man.draw(WIN)
	goblin.draw(WIN)
	for bullet in bullets:
		bullet.draw(WIN)
	pygame.display.update() #to refresh the window

#main loop
man = Player(300, 410, 64, 64)
goblin = Enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
while run:
	clock.tick(27) #the framerate for the game (fps)

	if shootLoop > 0:
		shoopLoop += 1
	if shootLoop > 3:
		shootLoop = 0

	for event in pygame.event.get(): #checking for events
		if event.type == pygame.QUIT:
			run = False

	for bullet in bullets:
		if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
			if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
				goblin.hit()
				bullets.pop(bullets.index(bullet))

		if bullet.x < screenWidth and bullet.x > 0:
			bullet.x += bullet.vel
		else:
			bullets.pop(bullets.index(bullet))

	keys = pygame.key.get_pressed() #to check key pressed (or held down)

	if shootLoop == 0 and keys[pygame.K_SPACE]:
		if man.left:
			facing = -1
		else:
			facing = 1
		if len(bullets) < 5:
			bullets.append(Projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0,0,0), facing))

		shootLoop = 1

	if keys[pygame.K_LEFT] and man.x > man.vel:
		man.x -= man.vel
		man.left = True
		man.right = False
		man.standing = False
	elif keys[pygame.K_RIGHT] and man.x < screenWidth - man.width - man.vel:
		man.x += man.vel
		man.right = True
		man.left = False
		man.standing = False
	else:
		man.staning = True
		man.walkCount = 0

	if not(man.isJump):
		if keys[pygame.K_UP]:
			man.isJump = True
			man.right = False
			man.left = False
			man.walkCount = 0
	else:
		if man.jumpCount >= -10:
			neg = 1
			if man.jumpCount < 0:
				neg = -1
			man.y -= neg * (man.jumpCount ** 2) * 0.5
			man.jumpCount -= 1
		else:
			man.isJump = False
			man.jumpCount = 10

	redrawGameWindow()


pygame.quit()
