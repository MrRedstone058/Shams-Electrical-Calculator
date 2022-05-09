import pygame
import math

pygame.init()

class Spritesheet():
	
	#initialiser
	def __init__(self, image):
		self.image = image
		
	#gets the current letter image with the given parameters
	def get_sprite(self, x, y, width, height):
		temp = pygame.Surface((width, height))
		temp.fill((254, 254, 254))
		temp.set_colorkey((254, 254, 254))
		temp.blit(self.image, (0, 0), (x, y, width, height))
		return temp
		
class Font():
	
	#initialiser
	def __init__(self, image, colour_separater, char_order, scale = 1):
		self.load_font(image, colour_separater, char_order, scale)
		
	#load font
	def load_font(self, image, colour_separater, char_order, scale):
		self.scale = scale
		self.char_order = char_order
		width = 0
		self.data = []
		x = 0
		for pixel in range(image.get_width()):
			if tuple(image.get_at((pixel, 0))) == colour_separater:
				self.data.append([x, 0, width, image.get_height()])
				x = pixel + 1
				width = 0
				continue
			else:
				width += 1
		self.font_s = Spritesheet(image)
		self.get_chars()
	
	#get data of location of each character image to be used later in the render function		
	def get_chars(self):
		chars = {}
		for index, item in enumerate(self.data):
			char = self.font_s.get_sprite(item[0], item[1], item[2], item[3])
			char = pygame.transform.scale(char, (char.get_width() * self.scale, char.get_height() * self.scale))
			chars[self.char_order[index]] = char
		self.chars = chars
		
	#draws text with the font on a specific surface	
	def render(self, text, pos, screen, offset):
		start_x = pos[0]
		start_y = pos[1]
		for letter in text:
			screen.blit(self.chars[letter], (start_x, start_y))
			start_x += (self.chars[letter].get_width() + offset)

	#changes the colour of the font
	def swap_palette(self, old, new):
		temp = pygame.Surface((self.font_s.image.get_width(), self.font_s.image.get_height()))
		temp2 = temp.copy()
		temp2.fill((0, 0, 1))
		temp2.blit(self.font_s.image, (0, 0))
		temp2.set_colorkey(old)
		temp.fill(new)
		temp.blit(temp2, (0, 0))
		temp.set_colorkey((0, 0, 1))
		self.font_s.image = temp.copy()
		self.get_chars()
	
	#get length of text in pixels	
	def get_length_pixels(self, text, offset):
		x = 0
		for letter in text:
			x += (self.chars[letter].get_width() + offset)
		x -= offset
		return x
		
class Button():
	
	#initialiser
	def __init__(self, rect, text, colour, text_colour, scale, id, image = None): #text is a list of lines of text
		self.text = text
		self.id = id
		self.colour = colour
		self.text_colour = text_colour
		self.rect = rect
		self.image = image
		self.font = Font(font_img, (223, 32, 32, 255), "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=~<>,./?:;\"'{}[]\|¬ ", scale)
		self.clicked = False
		self.pressed = False
		self.miss = False
		self.set()
		
	#set the locations to center the image or text
	def set(self):
		if not self.text_colour == (0, 0, 0):
			self.font.swap_palette((0, 0, 0), self.text_colour)
		if self.image:
			self.center = (self.rect.x + (self.rect.width / 2) - (self.image.get_width() / 2), self.rect.y + (self.rect.height / 2) - (self.image.get_height() / 2))
		else:
			self.center = []
			for text in self.text:
				self.center.append([self.rect.x + (self.rect.width / 2) - (self.font.get_length_pixels(text, 1) / 2), self.rect.y + (self.rect.height / 2) - (((10 * self.font.scale) * (len(self.text) - self.text.index(text))) - (5 * self.font.scale) * len(self.text))])
	
	#draws the button of a specific surface
	def draw(self, surface, position = None):
		if self.image:
			if position:
				pygame.draw.rect(surface, self.colour, pygame.Rect(position, (self.rect.width, self.rect.height)), 0, 3)
				surface.blit(self.image, position)
			else:
				pygame.draw.rect(surface, self.colour, self.rect, 0, 3)
				surface.blit(self.image, self.center)
		else:
			if position:
				pygame.draw.rect(surface, self.colour, pygame.Rect(position, (self.rect.width, self.rect.height)), 0, 3)
				for text in self.text:
					self.font.render(text, (position[0] + (self.rect.width / 2) - (self.font.get_length_pixels(text, 1) / 2), position[1] + (self.rect.height / 2) - (((10 * self.font.scale) * (len(self.text) - self.text.index(text))) - (5 * self.font.scale) * len(self.text))), surface, 1)
			else:
				pygame.draw.rect(surface, self.colour, self.rect, 0, 3)
				for text, pos in zip(self.text, self.center):
					self.font.render(text, pos, surface, 1)
	
	#functions that chanes the given text of button			
	def new_text(self, new_text, text_colour = None):
		self.text = new_text
		self.center = []
		if text_colour:
			self.font.swap_pallete(self.text_colour, text_colour)
		for text in self.text:
			self.center.append([self.rect.x + (self.rect.width / 2) - (self.font.get_length_pixels(text, 1) / 2), self.rect.y + (self.rect.height / 2) - (((10 * self.font.scale) * (len(self.text) - self.text.index(text))) - (5 * self.font.scale) * len(self.text))])
	
	#updates the button for mouse clicks
	def update(self, mdown, mx, my, position = None):
		self.clicked = False
		if mdown:
			if position:
				if pygame.Rect(position[0], position[1], self.rect.width, self.rect.height).collidepoint(mx, my):
					if not self.pressed:
						self.pressed = True
				else:
					if not self.miss:
						self.miss = True
			else:
				if self.rect.collidepoint(mx, my):
					if not self.pressed:
						self.pressed = True
				else:
					if not self.miss:
						self.miss = True
		else:
			if self.pressed:
				if not self.miss:
					self.clicked = True
				self.pressed = False
			if self.miss:
				self.miss = False
				
class Bill():
	
	#initialiser
	def __init__(self, name, meters = None):
		if meters is None:
			self.meters = {}
		else:
			self.meters = meters
		self.name = name
		
	#add meter
	def add_meter(self, meter_name):
		self.meters[meter_name] = Meter(meter_name)
		
	#remove meter
	def remove_meter(self, meter_name):
		if meter_name in self.meters:
			self.meters.pop(meter_name)
		
	#edit meter without renaming
	def edit_meter(self, old_meter_name, new_meter_name):
		self.meters[new_meter_name] = self.meters[old_meter_name]
		if not new_meter_name == old_meter_name:
			del self.meters[old_meter_name]
			
	#move appliance to another meter 
	def move_meter(self, old_name, new_name, obj_name):
		self.meters[new_name].items[obj_name] = self.meters[old_name].items[obj_name]
		del self.meters[old_name].items[obj_name]
		
	#edit meter with renaming
	def change_name_meter(self, old_name, new_name, obj_name, obj_new_name):
		self.meters[new_name].items[obj_new_name] = self.meters[old_name].items[obj_name]
		del self.meters[old_name].items[obj_name]
		
	#unused
	def load_file(self, file):
		pass
	
	#unused	
	def save_file(self):
		pass
		
class Meter():
	
	#initialiser
	def __init__(self, name):
		self.name = name
		self.items = {}
	
	#edit appliances		
	def edit(self, appliance, new_appliance, kwh, hour):
		self.items[new_appliance] = [kwh, hour]
		if not new_appliance == appliance:
			del self.items[appliance]
	
	#add appliances		
	def add_item(self, appliance, kwh, hour):
		self.items[appliance] = [kwh, hour]
	
	#remove appliance
	def remove_item(self, appliance):
		del self.items[appliance]
			
	#returns the total cost of the electric bill 
	def checkout(self, days):
		total = 0
		for item in self.items:
			less = (self.items[item][0] / 1000) * (self.items[item][1] * days)
			more = less - 200
			if more > 0:
				total += more * 0.492
			total += less * 0.218
		#total = format(total, "f")
		return total
	
	#overwrites the data of the bill with the given parameter, unused	
	def load_data(self, data):
		self.items = data

"""

**  THIS IS INCOMPLETE! DO NOT OPEN!	**

class Textbox():
	def __init__(self, rect):
		self.rect = rect
		self.text_edit = False
		self.name = ""
	
	def update(self, mdown, mx, my, max_x):
		if self.rect.collidepoint(mx, my) and mdown:
			if not self.text_edit:
				self.text_edit = True
		
		#keyboard input		
		if self.text_edit:
			name, current_letter, returned = keyboard(name, current_letter, max_x)
			if returned:
				self.text_edit = False
		if self.name in save_files:
			smol_font.render(c[4], (text_box[id].x, text_box[id].y + 15), surface, 1)
		if is_num:
			if len(name) > 0:
				try:
					num = float(name)
				except:
					smol_font.render(c[15], (text_box[id].x, text_box[id].y + (15 if name not in save_files else 30)), surface, 1)
					
					
	def draw(self):
		pygame.draw.rect(surface, (0, 0, 0), self.rect, 1)
		if self.text_edit:
			pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(text_box[id].x + 1 + get_x(name, smol_font.chars, 1, current_letter), text_box[id].y + 1, 1, 10))
		smol_font.render(name, (text_box[id].x + 2, text_box[id].y + 1), surface, 1)
					
"""

#miscs					
font_img = pygame.image.load("fonts.png")
smol_font = Font(font_img, (223, 32, 32, 255), "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=~<>,./?:;\"'{}[]\|¬ ")
