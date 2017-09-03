#!/usr/bin/python
#coding: latin-1

"""
                    GNU GENERAL PUBLIC LICENSE
                       Version 2, June 1991

 Copyright (C) 1989, 1991 Free Software Foundation, Inc., <http://fsf.org/>
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
"""

#Made by Mrpyfisher199: https://github.com/Mrpyfisher199

try:
	import pygame
except Exception as e:
	print "Sorry, it seems you dont have a library called pygame :(\nWould you like to download it (it will require your password)? (y/n)"
	an = raw_input("> ").upper()
	if an != "N":
		print "Starting"
		os.system("sudo -H pip install pygame")
		try:
			import pygame
			print 'You have successfully installed PYGAME!!!'
		except Exception as e:
			print "Looks like something went wrong :("
			quit()
	else:
		print "Well, thats a shame :("
		quit()

import pygame
pygame.init()

from random import randint as ran

w,h = 500,700
gameDisplay = pygame.display.set_mode((w,h))
pygame.display.set_caption('StarCorridor2')

green = (0,155,0)
red = (255,0,0)
silver=(179, 179, 179)
white = (255,255,255)
cyan = (11,99,250)
gold = (253,159,29)
black=(0,0,0)

effect = pygame.mixer.Sound('beep1.wav')

smallfont = pygame.font.Font("Fontspy/b.ttf", 10)
med1font = pygame.font.Font("Fontspy/c.ttf", 20)

a0 = pygame.sprite.Group()
a1 = pygame.sprite.Group()
a2 = pygame.sprite.Group()

clock = pygame.time.Clock()
fps=10


#Basically The Star
class Block(pygame.sprite.Sprite):
	def __init__(self, ws):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([20,20])
		self.image.fill(red)
		self.image.set_colorkey(red)
		self.rect = self.image.get_rect()
		self.rect.x = ws*20
		self.rect.y = 0
	def update(self):
		message_to_screen("#", red, (self.rect.x+10,self.rect.y), 0, "med")
		if self.rect.y > h:
			a0.remove(self)
		self.rect.y+=20
		
#The space Ship
class plane(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([60,20])
		self.image.fill(red)
		self.image.set_colorkey(red)
		self.rect = self.image.get_rect()
		self.image = pygame.Surface([20,20])
		self.image.fill(red)
		self.image.set_colorkey(red)
		self.rect1 = self.image.get_rect()
		self.rect.x = w/2-30
		self.rect1.x = w/2-10
		self.rect.y = 560-100
		self.rect1.y = 540-100
		self.move = 0
		self.health = 3


	def eventHan(self,event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				self.move = -20
			if event.key == pygame.K_RIGHT:
				self.move = 20


	def update(self):
		a1.update()
		a2.update()
		if self.move > 0 and self.rect.x+60+20 <= w:
			self.rect.x+=self.move
			self.rect1.x+=self.move
		if self.move < 0 and self.rect.x-20 >= 0:
			self.rect.x+=self.move
			self.rect1.x+=self.move
		self.move=0
		for i in a0:
			if (i.rect.x == self.rect.x or i.rect.x == self.rect.x+20 or i.rect.x == self.rect.x+40) and self.rect.y+20 == i.rect.y:
				a0.remove(i)
				self.health -= 1
				effect.play()
				gameDisplay.fill(red)
		message_to_screen("|",cyan,(self.rect1.x+10,self.rect1.y),0,"med")
		message_to_screen("__(+)__",cyan,(self.rect.x+30,self.rect.y),0,"med")
		message_to_screen("|",cyan,(self.rect.x,self.rect.y+16.5),0,"med")
		message_to_screen("|",cyan,(self.rect.x+60,self.rect.y+16.5),0,"med")
		bullet = Bullet(self.rect1.x)
		fire = Fire(self.rect.x)
		return self.health

#Train behind the space ship.
class Fire(pygame.sprite.Sprite):
	def __init__(self,x):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([20,20])
		self.image.fill(white)
		self.image.set_colorkey(white)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect1 = self.image.get_rect()
		self.rect1.x = x+40
		self.rect.y = 580-100
		self.rect1.y = 580-100
		self.color = red
		a2.add(self)

	def update(self):
		self.rect.y+=20
		self.rect1.y+=20
		if self.rect.y > h-60:
			self.color = white
		elif self.rect.y > h-140:
			self.color = gold
		if self.rect.y > h:
			a2.remove(self)
			return
		message_to_screen("+",self.color,(self.rect.x+5,self.rect.y-10),0,"med")
		message_to_screen("+",self.color,(self.rect1.x+15,self.rect1.y-10),0,"med")


#The Bullet...
class Bullet(pygame.sprite.Sprite):
	def __init__(self,x):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([20,20])
		self.image.fill(white)
		self.image.set_colorkey(white)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = 540-100
		a1.add(self)

	def update(self):
		self.rect.y-=20
		if self.rect.y < 0:
			a1.remove(self)
			return
		for i in a0:
			if i.rect.x == self.rect.x and i.rect.y == self.rect.y or i.rect.x == self.rect.x and i.rect.y+20 == self.rect.y:
				a1.remove(self)
				a0.remove(i)
				return
		#pygame.draw.ellipse(gameDisplay,white,(self.rect.x+5,self.rect.y-10,10,30))
		message_to_screen(":",white,(self.rect.x+10,self.rect.y-10),0,"med")

#Text Handling
def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "med":
        textSurface = med1font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color,a, y_displace, size):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (a[0]), (a[1])+y_displace
    gameDisplay.blit(textSurf, textRect)

#Display Health
def sHealth(health):
	color = green
	if health < 2:
		color = red
	elif health < 3:
		color = gold
	message_to_screen("Health: ["+''.join(["X" for i in range(3-health)])+''.join(["#" for i in range(health)])+"]",color,[w/2,h-30],0,"med")

#The Game
def game():
	#Count Down
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
	gameDisplay.fill(black)
	pygame.display.update()
	cnt=3
	while cnt > -1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(black)
		message_to_screen(str(cnt),red,[w/2-10,h/2-10],0,"med")
		pygame.display.update()
		clock.tick(1)
		cnt-=1
	#Game variables
	pause=False
	ttl = 5
	for i in range(25):
		att = ran(0,100)
		if att <= ttl:
			a0.add(Block(i))
	score=0
	Plane = plane()
	tck = 1
	health=3
	#The game itself...
	pygame.mixer.music.load('music.wav')
	pygame.mixer.music.set_volume(10)
	pygame.mixer.music.play(-1)
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RETURN:
					pause = not pause
			Plane.eventHan(event)
		gameDisplay.fill(black)
		if pause == False:
			#The Basic Logic...
			a0.update()
			if tck == 1:
				for i in range(25):
					att = ran(0,100)
					if att <= ttl:
						a0.add(Block(i))
				if ttl < 10:
					ttl += 0.25
				elif ttl < 50:
					ttl += 0.1
				elif ttl < 70:
					ttl+=0.05
				else:
					pass
				tck=-tck
				score+=1
			else:
				tck=-tck
			health = Plane.update()
		else:
			message_to_screen("PAUSED", red, [w/2,h/2], 0, "med")
		pygame.draw.rect(gameDisplay,gold,[0,10,w,40])
		pygame.draw.rect(gameDisplay,silver,[0,h-50,w,40])
		message_to_screen("Score: "+str(score),red,[w/2,28],0,"med")
		sHealth(health)
		pygame.display.update()
		clock.tick(fps)
		if health < 1:
			break
	#Game Over
	for i in range(20):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		gameDisplay.fill(black)
		message_to_screen("GAME OVER!!!", red, [w/2,h/2-100],0,"med")
		message_to_screen("Score: "+str(score),red,[w/2,h/2+100],0,"med")
		pygame.display.update()
		clock.tick(5)

game()
pygame.quit()