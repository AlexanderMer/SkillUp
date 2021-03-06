player = {
	'items' : [],
	'weapons' : [],
	'health' : 100.0
}
game = False
current_location = 'dark_room'
# Stracture of the level is as follows:
# level -> location -> rooms[]
#					-> items[] -> (name, id, description, actions)
#                              !!!!! Each action must be implemented
#------------------------------------------------
#
#
level = {
	'dark_room' : {
		'description' : 'a creepy and dark room',
		'rooms' : ['hallway'],
		'items' : [('a bucket','a very old leaky bucket')]
		},
	'hallway' : {
		'description' : 'an ordinary hallway with blinking lights',
		'rooms' : ['light_room', 'dark_room'],
		'items' : [('a bucket','a very old leaky bucket')]
		},
	'light_room' : {
		'description' : 'a brightly light room, it\'s so bright it hurts your eyes',
		'rooms' : ['hallway'],
		'items' : [('a bucket','a very old leaky bucket')]
		}
}




def goto(location):
	global current_location
	if location not in level[current_location]['rooms']:
		print('you can\'t go there from this location')
		return
	current_location = location
	print('you are in %s. %s' % (location, level[location]['description']))
	if len(level[location]['items']) > 0:
		if len(level[location]['items']) == 1:
			print('There is %s' % level[location]['items'][0][0])
		else:
			print('There are %s' % str(level[location]['items']))


#def showActions():
	#for a in level[current_location]['items']:
		
def take(item, location):
	print('You took %s.' % (item[0]))
	player['items'].append(item)
	level[location]['items'].remove(item)

def eat(food):
	player['health'] += food

def start():
	global game
	game = True
	goto('dark_room')
	while game:
		print('what would you like to do?')
		display_options()
		game = False


def display_options():
	if len(level[current_location]['items']) > 0:
		print('Take?')
	if len(level[current_location]['rooms']) > 0:
		print('Go?')
start()
	