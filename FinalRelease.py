import pygame
import classes
import importlib
import os
import settings
from captions import caption
pygame.init()

#get length of text of font in pixels
def get_x(text, data, offset, current):
	x = 0
	count = 0
	for char in text:
		if count == current:
			break
		else:
			count += 1
		x += data[char].get_width() + offset
	return x

#keyboard input
def keyboard(name, current_letter, max):
	global events, keys, src, dest
	returned = False
	for event in events:
		
		#key is pressed
		if event.type == pygame.KEYDOWN:
			
			#backspace
			if event.key == pygame.K_BACKSPACE:
				if current_letter > 0:
					if len(name) > 0:
						if current_letter == len(name):
							name = name[0:-1]
						else:
							name = f"{name[0:current_letter - 1]}{name[current_letter:len(name)]}"
						current_letter -= 1
						
			#enter
			elif event.key == pygame.K_RETURN:
				returned = True
				
			#left to move cursor
			elif event.key == pygame.K_LEFT:
				if current_letter > 0:
					current_letter -= 1
					
			#right to move cursor
			elif event.key == pygame.K_RIGHT:
				if current_letter < len(name):
					current_letter += 1
					
			#space
			elif event.key == pygame.K_SPACE:
				if current_letter == len(name):
					name = name + " "
				else:
					name = f"{name[0:current_letter]} {name[current_letter:len(name)]}"
				current_letter += 1
				
			#other normal keys
			else:
				if get_x(name, smol_font.chars, 1, len(name)) < max:
					
					#shift keys
					if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
						try:
							ch = chr(event.key)
							if ch in src:
								if current_letter == len(name):
									name = name + dest[src.index(ch)]
								else:
									name = f"{name[0:current_letter]}{dest[src.index(ch)]}{name[current_letter:len(name)]}"
								current_letter += 1
						except:
							pass
							
					#non shift keys
					else:
						try:
							if chr(event.key) in src:
								if current_letter == len(name):
									name = name + chr(event.key)
								else:
									name = f"{name[0:current_letter]}{event.unicode}{name[current_letter:len(name)]}"
								current_letter += 1
						except:
							pass
	return name, current_letter, returned

#cancel and ok menu	
def draw_sure(text, surface, rect = pygame.Rect(50, 75, 220, 60), pos1 = None, pos2 = None, text_y = 85, text_x = None):
	
	#x position for text
	if text_x is None:
		text_x = 160 - (smol_font.get_length_pixels(text, 1) / 2)
	clicked = False
	
	#draw prompt menu
	pygame.draw.rect(surface, (white), rect, 0, 3)
	pygame.draw.rect(surface, orange, rect, 1, 3)
	smol_font.render(text, (text_x, text_y), surface, 1)
	
	#yes and no buttons
	for button in create_button:
		if button.id == 0:
			if pos1:
				button.draw(surface, pos1)
				button.update(mdown, mx, my, pos1)
			else:
				button.draw(surface)
				button.update(mdown, mx, my)
		elif button.id == 1:
			if pos2:
				button.draw(surface, pos2)
				button.update(mdown, mx, my, pos2)	
			else:
				button.draw(surface)
				button.update(mdown, mx, my)
				
		#if any button is clicked
		if button.clicked:
			clicked = True
			
			#if cancel is clicked
			if button.id == 0:
				return False, clicked
				
			#if ok is clicked
			elif button.id == 1:
				return True, clicked
	return None, clicked

#reset language options
def reset_language(language):
	global orange, white, black
	#get dict of captions in current language
	c = caption[language].copy()
	
	#menu buttons
	m = [
	classes.Button(pygame.Rect(10, 40, 145, 85), [], orange, black, 1, 0, pygame.image.load("existing_invoices.png")), 
	classes.Button(pygame.Rect(165, 40, 145, 85), [], orange, black, 1, 1, pygame.image.load("new_invoice.png")),
	classes.Button(pygame.Rect(10, 125, 145, 45), c[1], orange, black, 1, 0), 
	classes.Button(pygame.Rect(165, 125, 145, 45), c[2], orange, black, 1, 1)
	]
	
	#cancel and ok buttons
	cr = [
	classes.Button(pygame.Rect(60, 120, 60, 12), c[7], white, black, 1, 0), 
	classes.Button(pygame.Rect(200, 120, 60, 12), c[8], white, black, 1, 1)
	]
	
	#edit buttons in edit menu
	l = []
	i = 5
	for a in range(7):
		t = c[a + 9]
		l.append([i, get_x(t, smol_font.chars, 1, len(t))])
		i += get_x(t, smol_font.chars, 1, len(t))
		i += 10
	e = [
	classes.Button(pygame.Rect(l[0][0], 1, l[0][1], 12), [c[9]], white, black, 1, 0), 
	classes.Button(pygame.Rect(l[1][0], 1, l[1][1], 12), [c[10]], white, black, 1, 1),
	classes.Button(pygame.Rect(l[2][0], 1, l[2][1], 12), [c[11]], white, black, 1, 2), 
	classes.Button(pygame.Rect(l[3][0], 1, l[3][1], 12), [c[12]], white, black, 1, 3),
	classes.Button(pygame.Rect(l[4][0], 1, l[4][1], 12), [c[13]], white, black, 1, 4),
	classes.Button(pygame.Rect(l[5][0], 1, l[5][1], 12), [c[15]], white, black, 1, 5),
	classes.Button(pygame.Rect(315 - get_x(c[14], smol_font.chars, 1, len(c[14])), 1, get_x(c[14], smol_font.chars, 1, len(c[14])), 12), [c[14]], white, black, 1, 6)
	]
	
	#setting buttons
	l = []
	i = 5
	for a in range(4):
		if len(c) >= a + 28:
			t = c[a + 28]
			l.append([i, get_x(t, smol_font.chars, 1, len(t))])
			i += get_x(t, smol_font.chars, 1, len(t))
			i += 10			
	k = []
	j = 5
	for a in range(3):
		if len(c) >= a + 32:
			t = c[a + 32]
			k.append([j, get_x(t, smol_font.chars, 1, len(t))])
			j += get_x(t, smol_font.chars, 1, len(t))
			j += 10
	s = [
	classes.Button(pygame.Rect(l[0][0], 1, l[0][1], 12), [c[28]], white, black, 1, 0), 
	classes.Button(pygame.Rect(l[1][0], 1, l[1][1], 12), [c[29]], white, black, 1, 1), 
	classes.Button(pygame.Rect(l[2][0], 1, l[2][1], 12), [c[30]], white, black, 1, 2),
	classes.Button(pygame.Rect(l[3][0], 1, l[3][1], 12), [c[31]], white, black, 1, 3),
	classes.Button(pygame.Rect(k[0][0], 167, k[0][1], 12), [c[32]], white, black, 1, 4),
	classes.Button(pygame.Rect(k[1][0], 167, k[1][1], 12), [c[33]], white, black, 1, 5),
	classes.Button(pygame.Rect(k[2][0], 167, k[2][1], 12), [c[34]], white, black, 1, 6)
	]
	
	i = [
	classes.Button(pygame.Rect(10, 1, get_x(c[9], smol_font.chars, 1, len(c[9])), 12), [c[9]], white, black, 1, 0),
	classes.Button(pygame.Rect(310 - get_x(c[43], smol_font.chars, 1, len(c[43])), 1, get_x(c[43], smol_font.chars, 1, len(c[43])), 12), [c[43]], white, black, 1, 1),
	classes.Button(pygame.Rect(160 - (get_x(c[44], smol_font.chars, 1, len(c[44])) / 2), 1, get_x(c[44], smol_font.chars, 1, len(c[44])), 12), [c[44]], white, black, 1, 2)

	]
	return c, m, cr, e, s, i

#draw textbox
def draw_textbox(id, surface, name, loc = [[], False], max = 195, is_num = False):
	global text_edit, c
	
	#if texbox is clicked
	if mdown:
		if text_box[id].collidepoint(mx, my):
			if not text_edit[id][0]:
				text_edit[id][0] = True
		else:
			text_edit[id][0] = False
			
	#keyboard input		
	pygame.draw.rect(surface, black, text_box[id], 1)
	if text_edit[id][0]:
		name, text_edit[id][1], returned = keyboard(name, text_edit[id][1], max)
		
		#enter is pressed
		if returned:
			text_edit[id][0] = False
		pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(text_box[id].x + 1 + get_x(name, smol_font.chars, 1, text_edit[id][1]), text_box[id].y + 1, 1, 10))
	smol_font.render(name, (text_box[id].x + 2, text_box[id].y + 1), surface, 1)
	
	#name is used prompt
	if name in loc[0]:
		if loc[1]:
			smol_font.render(c[4], (text_box[id].x, text_box[id].y + 15), surface, 1)
	
	#must be a number prompt
	if is_num:
		if len(name) > 0:
			try:
				num = float(name)
				is_num = True
			except:
				smol_font.render(c[27], (text_box[id].x, text_box[id].y + 15), surface, 1)
				is_num = False
	return name, is_num

def swap_palette(image, old, new): 
	temp = pygame.Surface((image.get_width(), image.get_height()))
	temp2 = temp.copy()
	temp2.fill((1, 1, 1))
	temp2.blit(image, (0, 0))
	temp2.set_colorkey(old)
	temp.fill(new)
	temp.blit(temp2, (0, 0))
	temp.set_colorkey((1, 1, 1))
	return temp
	
def convert_dark_mode(dark):
	if dark_mode:
		black = (170, 170, 170)
		white = (0, 0, 0)
		orange = "#904D00"
		temp_col = (0, 0, 0)
		temp_img_col = [(255, 255, 255), (170, 170, 170)]
		smol_font.swap_palette((0, 0, 0), (170, 170, 170))
		font.swap_palette((0, 0, 0), (170, 170, 170)) 
	else:
		black = (0, 0, 0)
		white = (255, 255, 255)
		orange = "#DF8020"
		temp_col = (170, 170, 170)
		temp_img_col = [(170, 170, 170), (255, 255, 255)]
		smol_font.swap_palette((170, 170, 170), (0, 0, 0))
		font.swap_palette((170, 170, 170), (0, 0, 0))
	
	#swap buton colours	
	for x in menu_buttons:
		x.colour = orange
		x.font.swap_palette(temp_col, black)
		if x.image:
			x.image = swap_palette(x.image, temp_img_col[0], temp_img_col[1])
	for x in create_button:
		x.colour = white
		x.font.swap_palette(temp_col, black)
	for x in edit_button:
		x.colour = white
		x.font.swap_palette(temp_col, black)
	for x in setting_button:
		x.colour = white
		x.font.swap_palette(temp_col, black)
	for x in invoice_button:
		x.colour = white
		x.font.swap_palette(temp_col, black)	
	return black, white, orange
	
#convert bills to text
def convert_to_txt(bill):
	string = "{"
	for meters in bill.meters:
		string = string + "'" + meters + "':" + "{"
		for appliances in bill.meters[meters].items:
			string = f"{string}'{appliances}': [{bill.meters[meters].items[appliances][0]}, {bill.meters[meters].items[appliances][1]}], "
		string = string + "}, "
	string = string + "}"
	return string

#convert dicts to bills	
def convert_to_bill(bill_data, bill_name):
	bill = classes.Bill(bill_name)
	for meter in bill_data[bill_name]:
		bill.add_meter(meter)
		for appliance in bill_data[bill_name][meter]:
			bill.meters[meter].add_item(appliance, bill_data[bill_name][meter][appliance][0], bill_data[bill_name][meter][appliance][1])
	return bill
		
def main():
	global orange, white, black, smol_font, dark_mode, font, menu_buttons, edit_button, create_button, setting_button, invoice_button, mdown, mx, my, text_box, text_edit, events, keys, src, dest, c
	#variables
	
	#booleans and none
	ch = None
	run = True
	mdown = False
	home = False
	add_name = False
	remove_name = False
	edit_name = False
	checkout = False
	move = False
	text_edit = False
	sure = False
	save = False
	prompt = False
	num = False
	is_kwh_num = False
	is_hours_num = False
	dark_mode = settings.settings[0]
	change_name = False
	add_meter = False
	remove_meter = False
	edit_meter = False
	total_checkout = False
	remove_bill = False
	edit_bill = False
	tax = settings.settings[2]
	set_sst = False
	set_days = False
	set_kwtbb = False
	
	#int
	sst = settings.settings[3] #0.06
	kwtbb = settings.settings[4] #0.016
	tax_val = sst + kwtbb
	days = settings.settings[5] #28
	
	#tuples
	screen_size = (320, 180)
	menu_colour = (255, 255, 255)
	black = (0, 0, 0)
	white = (255, 255, 255)
	
	#strings
	src = r"`1234567890-=qwertyuiop[]\asdfghjkl;\'zxcvbnm,./"
	dest = r'~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?'
	text = ""
	name = ""
	kwh = ""
	hours = ""
	new_name = ""
	file_name = ""
	temp_name = ""
	section = "menu"
	language = settings.settings[1]
	main_string = ""
	orange = "#DF8020" #(150, 150, 230) #"#DF8020"
	current_meter = "unassignedAppliances" 
	
	#lists
	save_files = []
	if os.path.exists("invoices.py"):
		import invoices
		for bills in invoices.invoice:
			save_files.append(bills)
	scroll = [0, 0, 0]
	
	#load fonts
	font_img = pygame.image.load("fonts.png")
	font = classes.Font(font_img, (223, 32, 32, 255), "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=~<>,./?:;\"'{}[]\|¬ ", 2)
	smol_font = classes.Font(font_img, (223, 32, 32, 255), "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+=~<>,./?:;\"'{}[]\|¬ ", 1)
	
	#get buttons
	c, menu_buttons, create_button, edit_button, setting_button, invoice_button = reset_language(language)
	
	#textboxes
	text_box = {
	0: pygame.Rect(59, 79, 202, 12),
	1: pygame.Rect(59, 29, 202, 12),
	2: pygame.Rect(59, 74, 202, 12),
	3: pygame.Rect(59, 119, 202, 12),
	4: pygame.Rect(24, 19, 202, 12),
	5: pygame.Rect(24, 64, 202, 12),
	6: pygame.Rect(24, 109, 202, 12),
	7: pygame.Rect(24, 154, 202, 12), 
	8: pygame.Rect(59, 49, 202, 12), 
	9: pygame.Rect(59, 94, 202, 12)
	}
	text_edit = {
	0: [False, 0],
	1: [False, 0], 
	2: [False, 0], 
	3: [False, 0],
	4: [False, 0],
	5: [False, 0],
	6: [False, 0],
	7: [False, 0], 
	8: [False, 0], 
	9: [False, 0]
	}
	
	#initialisation		
	screen = pygame.display.set_mode(screen_size, pygame.SCALED)
	display = pygame.Surface(screen_size)
	menu = pygame.Surface(screen_size)
	edit_menu = pygame.Surface(screen_size)
	invoice_menu = pygame.Surface(screen_size)
	setting_menu = pygame.Surface(screen_size)
	clock = pygame.time.Clock()
	black, white, orange = convert_dark_mode(dark_mode)
	
	while run:
		
		#mouse and key events
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mdown = True
			elif event.type == pygame.MOUSEBUTTONUP:
				mdown = False
				
			#if key is pressed and no prompt is shown
			elif event.type == pygame.KEYDOWN:
				if not any([text_edit[0][0], text_edit[1][0], text_edit[2][0], text_edit[3][0], text_edit[4][0], text_edit[5][0], text_edit[6][0], text_edit[7][0], text_edit[8][0], text_edit[9][0]]):
					
					#malay language
					if event.key == pygame.K_m:
						if language == "english":
							language = "malay"
							c, menu_buttons, create_button, edit_button, setting_button, invoice_button = reset_language("malay")
							black, white, orange = convert_dark_mode(dark_mode)
					
					#english language
					elif event.key == pygame.K_e:
						if language == "malay":
							language = "english"
							c, menu_buttons, create_button, edit_button, setting_button, invoice_button = reset_language("english")
							black, white, orange = convert_dark_mode(dark_mode)
						
					#dark mode
					elif event.key == pygame.K_d:
						dark_mode = not dark_mode
						black, white, orange = convert_dark_mode(dark_mode)
					
					#tax
					elif event.key == pygame.K_t:
						tax = not tax
		
		#get pressed keys and mouse position			
		mx, my = pygame.mouse.get_pos()
		keys = pygame.key.get_pressed()	
		display.fill(menu_colour)
		
		#menu
		if section == "menu":
			display.blit(menu, (0, 0))
			menu.fill(white)
			pygame.draw.rect(menu, orange, pygame.Rect(10, 120, 145, 10), 0, 3)
			pygame.draw.rect(menu, orange, pygame.Rect(165, 120, 145, 10), 0, 3)
			for button in menu_buttons:
				button.draw(menu)
			text = c[0]
			font.render(text, (160 - (font.get_length_pixels(text, 1) / 2), 10), menu, 1)
			
			#handle buttons
			if not prompt:
				for button in menu_buttons:
					button.update(mdown, mx, my)
					if button.clicked:
						
						#existing invoices
						if button.id == 0:
							section = "select invoice"
							
						#create new invoice
						if button.id == 1:
							prompt = True
						
			#make new list
			if prompt:
				
				#sets menu to slightly transparent
				menu.set_alpha(127)
				yes, clicked = draw_sure(c[3], display, pygame.Rect(50, 55, 220, 80), (60, 120), (200, 120), 65)
				name, _ = draw_textbox(0, display, name, [save_files, True], 195)
					
				#cancel and ok
				if clicked:
					if yes:
						if name not in save_files:
							if len(name) > 0:
								section = "edit list"
								prompt = False
								bill = classes.Bill(name, {"unassignedAppliances": classes.Meter("unassignedAppliances")})
								file_name = name
								name = ""
								text_edit[0] = [False, 0]
					else:
						text_edit[0][1] = 0
						prompt = False
						name = ""
						text_edit[0] = [False, 0]
			else:
				#full opacity
				menu.set_alpha(255)
			
		#edit menu	
		elif section == "edit list":
			if keys[pygame.K_UP]:
				if scroll[1] > 0:
					scroll[1] -= 2
					scroll[1] = max(scroll[1], 0)
			if keys[pygame.K_DOWN]:
				if 34 + (13 * len(bill.meters[current_meter].items)) > 180:
					scroll[1] += 2
					scroll[1] = min(scroll[1], max(0, (13 * len(bill.meters[current_meter].items) - 147)))
			display.blit(edit_menu, (0, 0))
			edit_menu.fill(orange)
			
			#draw table
			if len(bill.meters[current_meter].items) > 0:
				
				#draws the headers
				smol_font.render(c[22], (6, 21 - scroll[1]), edit_menu, 1)
				smol_font.render(c[23], (198, 21 - scroll[1]), edit_menu, 1)
				smol_font.render(c[24], (258, 21 - scroll[1]), edit_menu, 1)
				
				#draws the grids
				pygame.draw.line(edit_menu, white, (4, min(19, 19 - scroll[1])), (4, min(screen_size[1], 32 + len(bill.meters[current_meter].items) * 13)))
				pygame.draw.line(edit_menu, white, (316, min(19, 19 - scroll[1])), (316, min(screen_size[1], 32 + len(bill.meters[current_meter].items) * 13)))
				pygame.draw.line(edit_menu, white, (256, min(19, 19 - scroll[1])), (256, min(screen_size[1], 32 + len(bill.meters[current_meter].items) * 13)))
				pygame.draw.line(edit_menu, white, (196, min(19, 19 - scroll[1])), (196, min(screen_size[1], 32 + len(bill.meters[current_meter].items) * 13)))
				
				#splitlines for each appliance	
				for y in range(min(int((screen_size[1] - 19) / 13), len(bill.meters[current_meter].items)) + 2):
					loc_y = 19 + ((y * 13) - (scroll[1] % 13))
					pygame.draw.line(edit_menu, white, (4, loc_y), (316, loc_y))
				
				#names for each appliance	
				for idx, appliances in enumerate(bill.meters[current_meter].items):
					loc_y = 34 + (idx * 13) - scroll[1]
					if loc_y > 0:
						smol_font.render(appliances, (6, loc_y), edit_menu, 1)
						smol_font.render(str(bill.meters[current_meter].items[appliances][0]), (198, loc_y), edit_menu, 1)
						smol_font.render(str(bill.meters[current_meter].items[appliances][1]), (258, loc_y), edit_menu, 1)
					
			#draw button options
			pygame.draw.rect(edit_menu, white, pygame.Rect(0, 1, 320, 12))
			pygame.draw.line(edit_menu, black, (0, 13), (320, 13))
			pygame.draw.line(edit_menu, black, (0, 0), (320, 0))
			for button in edit_button:
				button.draw(edit_menu)
				button.update(mdown, mx, my)
				if not prompt:
					if button.clicked:
						
						#home
						if button.id == 0:
							home = True
							prompt = True
							
						#add appliance
						if button.id == 1:
							add_name = True
							prompt = True
							
						#remove appliance
						if button.id == 2:
							if len(bill.meters[current_meter].items) > 0:
								remove_name = True
								prompt = True
								
						#edit appliance
						if button.id == 3:
							if len(bill.meters[current_meter].items) > 0:
								edit_name = True
								prompt = True
								
						#checkout current meter
						if button.id == 4:
							checkout = True
							prompt = True
							
						#move appliance to another meter
						if button.id == 5:
							if len(bill.meters[current_meter].items) > 0:
								move = True
								prompt = True
							
						#settings
						if button.id == 6:
							section = "settings"
			
			#modes
			if any([home, sure, add_name, remove_name, edit_name, checkout, move, change_name]):
				
				#sets menu to slightly transparent
				edit_menu.set_alpha(127)
				
				#home prompt
				if home:
					yes, clicked = draw_sure(c[5], display)
					if clicked:
						if yes:
							sure = True
						else:
							sure = False
							prompt = False
						home = False
				
				#save file prompt
				elif sure:
					yes, clicked = draw_sure(c[6], display)
					if clicked:
						if yes:
							save = True
						else:
							save = False
							
						#save file
						if save:
							
							#file does not exist
							if not os.path.exists("invoices.py"):
								file = open("invoices.py", "w")
								string = "invoice = {'" + file_name + "':" + convert_to_txt(bill) + "}"
								file.write(string)
								file.close()
								
							#file exist
							else:
								if len(invoices.invoice) > 0:
									temp = []
									for item in invoices.invoice:
										temp.append(convert_to_bill(invoices.invoice, item))
									string = "invoice = {"
									if not file_name in temp:
										string = string + "'" + file_name + "':" + convert_to_txt(bill) + ","
										n = True
									else:
										n = False
									for item in temp:
										if item.name == file_name:
											if not n:
												string = string + "'" + file_name + "':" + convert_to_txt(bill) + ","
										else:
											string = string + "'" + item.name + "':" + convert_to_txt(item) + ","
									string = string + "}"
									file = open("invoices.py", "w")
									file.write(string)
									file.close()
								else:
									file = open("invoices.py", "w")
									string = "invoice = {'" + file_name + "':" + convert_to_txt(bill) + "}"
									file.write(string)
									file.close()
									
							#reload file
							import invoices
							importlib.reload(invoices)
							save_files = []
							files = invoices.invoice
							for file in files:
								save_files.append(file)
								
						#return to main menu
						section = "menu"
						sure = False
						prompt = False
				
				#appliance exists already in another meter
				elif change_name:
					
					#draw prompt
					yes, clicked = draw_sure(c[49], display, pygame.Rect(50, 60, 220, 70), (60, 110), (200, 110), 65, 60)
					temp_name, _ = draw_textbox(0, display, temp_name, [bill.meters[new_name].items, True], 180)
					
					#if clicked
					if clicked:
						if yes:
							if len(temp_name) > 0:
								if not temp_name in bill.meters[new_name].items:
									bill.change_name_meter(current_meter, new_name, name, temp_name)
									if scroll[1] > 0:
										scroll[1] -= min(scroll[1], 13)
									change_name = False
									prompt = False
									name = ""
									new_name = ""
									temp_name = ""
									text_edit[0] = [False, 0]
									
						else:
							change = False
							prompt = False
							name = ""
							new_name = ""
							temp_name = ""
							text_edit[0] = [False, 0]
							
				#move appliance prompt
				elif move:
					
					#draw prompt
					yes, clicked = draw_sure(c[47], display, pygame.Rect(50, 25, 220, 130), (60, 135), (200, 135), 35, 60)
					name, _ = draw_textbox(8, display, name, [[], False], 180)
					smol_font.render(c[48], (60, 80), display, 1)
					new_name, _ = draw_textbox(9, display, new_name, [[], False])
					if len(name) > 0:
						if name not in bill.meters[current_meter].items:
							smol_font.render(c[21], (60, 65), display, 1)
					if len(new_name) > 0:
						if new_name not in bill.meters:
							smol_font.render(c[21], (60, 110), display, 1)
					
					#if clicked
					if clicked:
						if yes:
							if len(name) > 0 and len(new_name) > 0 and new_name in bill.meters:
								
								#if appliance exist in another file
								if name in bill.meters[new_name].items:
									change_name = True
											
								#successful
								elif name in bill.meters[current_meter].items and new_name in bill.meters:
									bill.move_meter(current_meter, new_name, name)
									prompt = False
									name = ""
									new_name = ""
									if scroll[1] > 0:
										scroll[1] -= min(scroll[1], 13)
								move = False
								text_edit[8] = [False, 0]
								text_edit[9] = [False, 0]
						else:
							move = False
							prompt = False
							name = ""
							new_name = ""
							text_edit[8] = [False, 0]
							text_edit[9] = [False, 0]
				
				#add appliance prompt
				elif add_name:
					
					#draw prompt
					yes, clicked = draw_sure(c[16], display, pygame.Rect(50, 10, 220, 160), (60, 155), (200, 155), 15, 60)
					name, _ = draw_textbox(1, display, name, [bill.meters[current_meter].items, True], 180)
					smol_font.render(c[17], (60, 60), display, 1)
					kwh, is_kwh_num = draw_textbox(2, display, kwh, [[], False], 50, True)
					smol_font.render(c[18], (60, 105), display, 1)
					hours, is_hours_num = draw_textbox(3, display, hours, [[], False], 50, True)
					
					#if clicked
					if clicked:
						if yes:
							if len(name) > 0 and len(kwh) > 0 and len(hours) > 0:
								if name not in bill.meters[current_meter].items and is_kwh_num and is_hours_num:
									bill.meters[current_meter].add_item(name, float(kwh), float(hours))
									add_name = False
									prompt = False
									name = ""
									kwh = ""
									hours = ""
									text_edit[1] = [False, 0]
									text_edit[2] = [False, 0]
									text_edit[3] = [False, 0]
						else:
							add_name = False
							prompt = False
							name = ""
							kwh = ""
							hours = ""
							text_edit[1] = [False, 0]
							text_edit[2] = [False, 0]
							text_edit[3] = [False, 0]
						
				#remove appliance prompt
				elif remove_name:
					
					#draw prompt
					yes, clicked = draw_sure(c[25], display, pygame.Rect(50, 60, 220, 70), (60, 110), (200, 110), 65, 60)
					name, _ = draw_textbox(0, display, name, [[], False], 180)
					if len(name) > 0:
						if name not in bill.meters[current_meter].items:
							smol_font.render(c[21], (60, 95), display, 1)
					
					#if clicked
					if clicked:
						if yes:
							if len(name) > 0:
								if name in bill.meters[current_meter].items:
									bill.meters[current_meter].remove_item(name)
									if scroll[1] > 0:
										scroll[1] -= min(scroll[1], 13)
									remove_name = False
									prompt = False
									name = ""
									text_edit[0] = [False, 0]
									
						else:
							remove_name = False
							prompt = False
							name = ""
							text_edit[0] = [False, 0]
					
				#edit appliance prompt
				elif edit_name:
					
					#draw prompt
					yes, clicked = draw_sure(c[20], display, pygame.Rect(20, 0, 280, 180), (235, 130), (235, 40), 5, 25)
					name, _ = draw_textbox(4, display, name, [[], False], 180)
					smol_font.render(c[19], (25, 50), display, 1)
					new_name, _ = draw_textbox(5, display, new_name, [[], False])
					smol_font.render(c[17], (25, 95), display, 1)
					kwh, is_kwh_num = draw_textbox(6, display, kwh, [[], False], 60, True)
					smol_font.render(c[18], (25, 135), display, 1)
					hours, is_hours_num = draw_textbox(7, display, hours, [[], False], 60, True)
					if len(name) > 0:
						if name not in bill.meters[current_meter].items:
							smol_font.render(c[21], (25, 35), display, 1)
						if new_name in bill.meters[current_meter].items and not name == new_name:
							smol_font.render(c[4], (25, 80), display, 1)
						
					#if clicked	
					if clicked:
						if yes:
							if len(name) > 0 and len(kwh) > 0 and len(hours) > 0 and len(new_name) > 0:
								if name in bill.meters[current_meter].items and (new_name not in bill.meters[current_meter].items or (new_name in bill.meters[current_meter].items and new_name == name)) and is_kwh_num and is_hours_num:
									bill.meters[current_meter].edit(name, new_name, float(kwh), float(hours))
									edit_name = False
									prompt = False
									name = ""
									kwh = ""
									hours = ""
									new_name = ""
									text_edit[4] = [False, 0]
									text_edit[5] = [False, 0]
									text_edit[6] = [False, 0]
									text_edit[7] = [False, 0]
						else:
							edit_name = False
							prompt = False
							name = ""
							kwh = ""
							hours = ""
							new_name = ""
							text_edit[4] = [False, 0]
							text_edit[5] = [False, 0]
							text_edit[6] = [False, 0]
							text_edit[7] = [False, 0]
							
				#checkout prompt
				elif checkout:
					
					#draw prompt
					total = bill.meters[current_meter].checkout(days)
					if tax:
						yes, clicked = draw_sure(c[53], display, pygame.Rect(50, 60, 220, 70), (-60, 110), (130, 110), 75)
						tax_val = sst + kwtbb
						total += (total * tax_val)
					else:
						yes, clicked = draw_sure(c[26], display, pygame.Rect(50, 60, 220, 70), (-60, 110), (130, 110), 75)
					total = f"RM {total}"
					smol_font.render(total, ((160 - get_x(total, smol_font.chars, 1, len(total)) / 2), 90), display, 1)
					if clicked:
						if yes:		
							checkout = False
							prompt = False
					
			#full opacity
			else:
				edit_menu.set_alpha(255)
		
		#invoice selection menu				
		elif section == "select invoice":
			pygame.draw.rect(invoice_menu, white, pygame.Rect(0, 1, 320, 12))
			pygame.draw.line(invoice_menu, black, (0, 13), (320, 13))
			pygame.draw.line(invoice_menu, black, (0, 0), (320, 0))
			for button in invoice_button:
				button.draw(invoice_menu)
				button.update(mdown, mx, my)
				if not prompt:
					if button.clicked:
						if button.id == 0:
							section = "menu"
						if button.id == 1:
							if len(save_files) > 0:
								remove_bill = True
								prompt = True
						if button.id == 2:
							if len(save_files) > 0:
								edit_bill = True
								prompt = True
							
			display.blit(invoice_menu, (0, 0))
			invoice_menu.fill(orange)
			
			#scroll with keyboard
			if keys[pygame.K_UP]:
				if scroll[2] > 0:
					scroll[2] -= 2
					scroll[2] = max(scroll[2], 0)
			if keys[pygame.K_DOWN]:
				if 34 + (15 * len(save_files)) > 180:
					scroll[2] += 2
					scroll[2] = min(scroll[2], max(0, (15 * len(save_files)) - 160))
					
			#draw all meters
			for i, meters in enumerate(save_files):
				loc_y = (19 + (15 * i)) - scroll[2]
				rect = pygame.Rect(0, (loc_y) - 2, 320, 14)
				
				#if meter is in the screen
				if rect.y > 0 and rect.y < 180:
					smol_font.render(meters, (5, loc_y), invoice_menu, 1)
					if mdown:
						
						#if meter is selected
						if rect.collidepoint(mx, my):
							if not any([remove_bill, edit_bill]):
								section = "edit list"
								bill = convert_to_bill(invoices.invoice, meters)
								file_name = meters
			
			#modes
			if any([remove_bill, edit_bill]):
				
				#set the menu to slightly transparent
				invoice_menu.set_alpha(127)
				
				#remove bill prompt
				if remove_bill:
					
					#draw prompt
					yes, clicked = draw_sure(c[45], display, pygame.Rect(50, 60, 220, 70), (60, 110), (200, 110), 65, 60)
					name, _ = draw_textbox(0, display, name, [[], False], 180)
					if len(name) > 0:
						if name not in save_files:
							smol_font.render(c[21], (60, 95), display, 1)
					
					#if clicked
					if clicked:
						if yes:
							if len(name) > 0:
								if name in save_files:
										
									#file exist
									if len(invoices.invoice) > 0:
										temp = []
										for item in invoices.invoice:
											temp.append(convert_to_bill(invoices.invoice, item))
										string = "invoice = {"
										
										for item in temp:
											if item.name == name:
												continue
											else:
												string = string + "'" + item.name + "':" + convert_to_txt(item) + ","
										string = string + "}"
										file = open("invoices.py", "w")
										file.write(string)
										file.close()
											
									#reload file
									import invoices
									importlib.reload(invoices)
									save_files = []
									files = invoices.invoice
									for file in files:
										save_files.append(file)
										
									remove_bill = False
									prompt = False
									name = ""
									text_edit[0] = [False, 0]
									
						else:
							remove_bill = False
							prompt = False
							name = ""
							text_edit[0] = [False, 0]
					
				#edit meter prompt
				elif edit_bill:
					
					#draw prompt
					yes, clicked = draw_sure(c[50], display, pygame.Rect(50, 25, 220, 130), (60, 135), (200, 135), 35, 60)
					name, _ = draw_textbox(8, display, name, [[], False], 180)
					smol_font.render(c[51], (60, 80), display, 1)
					new_name, _ = draw_textbox(9, display, new_name, [[], False])
					if len(name) > 0:
						if name not in save_files:
							smol_font.render(c[21], (60, 65), display, 1)
						if new_name in save_files and not name == new_name:
							smol_font.render(c[4], (60, 110), display, 1)
							
					#if clicked
					if clicked:
						if yes:
							if len(name) > 0:
								if name in save_files and (new_name not in save_files or (new_name in save_files and new_name == name)):
									 
									#file exist
									if len(invoices.invoice) > 0:
										temp = []
										for item in invoices.invoice:
											temp.append(convert_to_bill(invoices.invoice, item))
										string = "invoice = {"
										
										for item in temp:
											if item.name == name:
												string = string + "'" + new_name + "':" + convert_to_txt(item) + ","
											else:
												string = string + "'" + item.name + "':" + convert_to_txt(item) + ","
										string = string + "}"
										file = open("invoices.py", "w")
										file.write(string)
										file.close()
											
									#reload file
									import invoices
									importlib.reload(invoices)
									save_files = []
									files = invoices.invoice
									for file in files:
										save_files.append(file)
										
									edit_bill = False
									prompt = False
									name = ""
									new_name = ""
									text_edit[8] = [False, 0]
									text_edit[9] = [False, 0]
						else:
							edit_bill = False
							prompt = False
							name = ""
							new_name = ""
							text_edit[8] = [False, 0]
							text_edit[9] = [False, 0]
							
			#full opacity
			else:
				invoice_menu.set_alpha(255)
										
		#settings
		elif section == "settings":
			pygame.draw.rect(setting_menu, white, pygame.Rect(0, 1, 320, 12))
			pygame.draw.line(setting_menu, black, (0, 13), (320, 13))
			pygame.draw.line(setting_menu, black, (0, 0), (320, 0))
			pygame.draw.rect(setting_menu, white, pygame.Rect(0, 167, 320, 12))
			pygame.draw.line(setting_menu, black, (0, 166), (320, 166))
			pygame.draw.line(setting_menu, black, (0, 179), (320, 179))
			
			#draw button options
			for button in setting_button:
				button.draw(setting_menu)
				button.update(mdown, mx, my)
				if not prompt:
					if button.clicked:
						
						#back
						if button.id == 0:
							section = "edit list"
							
						#add meter
						if button.id == 1:
							add_meter = True
							prompt = True
							
						#remove meter
						if button.id == 2:
							remove_meter = True
							prompt = True
							
						#edit meter
						if button.id == 3:
							edit_meter = True
							prompt = True
							
						#toggle language
						if button.id == 4:
							if language == "malay":
								language = "english"
							else:
								language = "malay"
							c, menu_buttons, create_button, edit_button, setting_button, invoice_button = reset_language(language)
							black, white, orange = convert_dark_mode(dark_mode)
						
						#dark mode
						if button.id == 5:
							dark_mode = not dark_mode
							black, white, orange = convert_dark_mode(dark_mode)
							
						#check the price for all meters
						if button.id == 6:
							total_checkout = True
							prompt = True
				
			#scroll with keyboard
			if keys[pygame.K_UP]:
				if scroll[0] > 0:
					scroll[0] -= 2
					scroll[0] = max(scroll[0], 0)
			if keys[pygame.K_DOWN]:
				if 34 + (15 * len(bill.meters)) > 167:
					scroll[0] += 2
					scroll[0] = min(scroll[0], max(0, (15 * len(bill.meters)) - 120))
					
			#set sst, kwtbb and days buttons
			if not prompt:
								
				#set sst
				if keys[pygame.K_s]:
					set_sst = True
					prompt = True
				
				#set days	
				elif keys[pygame.K_g]:
					set_days = True
					prompt = True
				
				#set kwtbb
				elif keys[pygame.K_k]:
					set_kwtbb = True
					prompt = True
				
			display.blit(setting_menu, (0, 0))
			setting_menu.fill(orange)
			
			#displays all meters
			smol_font.render(f"{c[46]} {file_name}", (5, 19 - scroll[0]), setting_menu, 1)
			smol_font.render(c[35], (5, 34 - scroll[0]), setting_menu, 1)
			smol_font.render(f"{c[57]} {sst}", (85, 34 - scroll[0]), setting_menu, 1)
			smol_font.render(f"{c[58]} {kwtbb}", (165, 34 - scroll[0]), setting_menu, 1)
			smol_font.render(f"{c[59]} {days}", (245, 34 - scroll[0]), setting_menu, 1)
			for i, rect in enumerate([pygame.Rect(85, 34 - scroll[0], 60, 15), pygame.Rect(165, 34 - scroll[0], 60, 15), pygame.Rect(245, 34 - scroll[0], 60, 15)]):
				if mdown:
					if rect.collidepoint(mx, my):
						if not prompt:
							if i == 0:
								set_sst = True
							if i == 1:
								set_kwtbb = True
							if i == 2:
								set_days = True
							prompt = True
							
			pygame.draw.line(setting_menu, white, (0, 46 - scroll[0]), (320, 46 - scroll[0]))
			for i, meters in enumerate(bill.meters):
				loc_y = (49 + (15 * i)) - scroll[0]
				rect = pygame.Rect(0, (loc_y) - 2, 320, 14)
				
				#if meter is in the screen
				if current_meter in bill.meters:
					if rect.y > 0 and rect.y < 166:
						smol_font.render(meters, (5, loc_y), setting_menu, 1)
						if mdown:
							
							#if meter is selected
							if rect.collidepoint(mx, my):
								if not prompt:
									current_meter = meters
									scroll[1] = 0
				else:
					current_meter = "unassignedAppliances"
					scroll[1] = 0
					
				#draws red box
				if meters == current_meter:
					pygame.draw.rect(setting_menu, (255, 0, 0), rect, 1)
					
			#modes
			if any([add_meter, remove_meter, edit_meter, total_checkout, set_sst, set_kwtbb, set_days]):
				
				#sets menu to slightly transparent
				setting_menu.set_alpha(127)
						
				#add meter prompt
				if add_meter:
					
					#draw prompt
					yes, clicked = draw_sure(c[36], display, pygame.Rect(50, 60, 220, 70), (60, 110), (200, 110), 65, 60)
					name, _ = draw_textbox(0, display, name, [bill.meters, True], 180)
					
					#if clicked
					if clicked:
						if yes:
							if len(name) > 0:
								if name not in bill.meters:
									bill.add_meter(name)
									add_meter = False
									prompt = False
									name = ""
									text_edit[0] = [False, 0]
									
						else:
							add_meter = False
							prompt = False
							name = ""
							text_edit[0] = [False, 0]
						
				#remove meter prompt
				elif remove_meter:
					
					#draw prompt
					yes, clicked = draw_sure(c[37], display, pygame.Rect(50, 60, 220, 70), (60, 110), (200, 110), 65, 60)
					name, _ = draw_textbox(0, display, name, [[], False], 180)
					if len(name) > 0:
						if name not in bill.meters:
							smol_font.render(c[21], (60, 95), display, 1)
						elif name == "unassignedAppliances":
							smol_font.render(c[38], (60, 95), display, 1)
					
					#if clicked
					if clicked:
						if yes:
							if len(name) > 0:
								if name in bill.meters and not name == "unassignedAppliances":
									bill.remove_meter(name)
									if scroll[0] > 0:
										scroll[0] -= min(scroll[0], 15)
									remove_meter = False
									prompt = False
									name = ""
									text_edit[0] = [False, 0]
									
						else:
							remove_meter = False
							prompt = False
							name = ""
							text_edit[0] = [False, 0]
					
				#edit meter prompt
				elif edit_meter:
					
					#draw prompt
					yes, clicked = draw_sure(c[39], display, pygame.Rect(50, 25, 220, 130), (60, 135), (200, 135), 35, 60)
					name, _ = draw_textbox(8, display, name, [[], False], 180)
					smol_font.render(c[40], (60, 80), display, 1)
					new_name, _ = draw_textbox(9, display, new_name, [[], False])
					if len(name) > 0:
						if name not in bill.meters:
							smol_font.render(c[21], (60, 65), display, 1)
						if new_name in bill.meters and not name == new_name:
							smol_font.render(c[4], (60, 110), display, 1)
						if name == "unassignedAppliances":
							smol_font.render(c[41], (60, 65), display, 1)
							
					#if clicked
					if clicked:
						if yes:
							if len(name) > 0 and not name == "unassignedAppliances":
								if name in bill.meters and (new_name not in bill.meters or (new_name in bill.meters and new_name == name)): 
									bill.edit_meter(name, new_name)
									edit_meter = False
									prompt = False
									name = ""
									new_name = ""
									text_edit[8] = [False, 0]
									text_edit[9] = [False, 0]
						else:
							edit_meter = False
							prompt = False
							name = ""
							new_name = ""
							text_edit[8] = [False, 0]
							text_edit[9] = [False, 0]
							
				#checkout prompt
				elif total_checkout:
					total = 0
					for meter in bill.meters:
						total += bill.meters[meter].checkout(days)
					if tax:
						tax_val = sst + kwtbb
						total += total * tax_val
						yes, clicked = draw_sure(c[52], display, pygame.Rect(50, 60, 220, 70), (-60, 110), (130, 110), 75)
					else:
						yes, clicked = draw_sure(c[42], display, pygame.Rect(50, 60, 220, 70), (-60, 110), (130, 110), 75)
					total = f"RM {total}"
					smol_font.render(total, ((160 - get_x(total, smol_font.chars, 1, len(total)) / 2), 90), display, 1)
					if clicked:
						if yes:		
							total_checkout = False
							prompt = False
							
				#set sst
				elif set_sst:
					
					#draw prompt
					yes, clicked = draw_sure(c[54], display, pygame.Rect(50, 60, 220, 70), (60, 110), (200, 110), 65, 60)
					name, is_num = draw_textbox(0, display, name, [[], True], 30, True)
					
					#if clicked
					if clicked:
						if yes:
							if len(name) > 0:
								if is_num:
									sst = float(name)
									set_sst = False
									prompt = False
									name = ""
									text_edit[0] = [False, 0]
									
						else:
							set_sst = False
							prompt = False
							name = ""
							text_edit[0] = [False, 0]
				
				#set kwtbb
				elif set_kwtbb:
					
					#draw prompt
					yes, clicked = draw_sure(c[55], display, pygame.Rect(50, 60, 220, 70), (60, 110), (200, 110), 65, 60)
					name, is_num = draw_textbox(0, display, name, [[], True], 30, True)
					
					#if clicked
					if clicked:
						if yes:
							if len(name) > 0:
								if is_num:
									kwtbb = float(name)
									set_kwtbb = False
									prompt = False
									name = ""
									text_edit[0] = [False, 0]
									
						else:
							set_kwtbb = False
							prompt = False
							name = ""
							text_edit[0] = [False, 0]
							
				#set days
				elif set_days:
					
					#draw prompt
					yes, clicked = draw_sure(c[56], display, pygame.Rect(50, 60, 220, 70), (60, 110), (200, 110), 65, 60)
					name, is_num = draw_textbox(0, display, name, [[], True], 30, True)
					
					#if clicked
					if clicked:
						if yes:
							if len(name) > 0:
								if is_num:
									days = float(name)
									set_days = False
									prompt = False
									name = ""
									text_edit[0] = [False, 0]
									
						else:
							set_days = False
							prompt = False
							name = ""
							text_edit[0] = [False, 0]
							
			#full opacity
			else:
				setting_menu.set_alpha(255)
			
		#take off the comment on the line after if you want to enable fps		
		#smol_font.render(str(round(clock.get_fps())), (0, 20), display, 1)
		screen.blit(display, (0, 0))
		clock.tick(60)
		pygame.display.update()
	with open("settings.py", "w") as file:
		file.write(f"settings = [{dark_mode}, '{language}', {tax}, {sst}, {kwtbb}, {days}]")
	pygame.quit()
	
if __name__ == "__main__":
	main()