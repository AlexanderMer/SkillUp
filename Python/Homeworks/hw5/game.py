player = {
	'items' : [],
	'weapons' : [],
	'health' : 100.0
}
# Stracture of the level is as follows:
# level -> location -> rooms[]
#					-> items[] -> (name, id, description, actions)
#                              !!!!! Each action must be implemented
#------------------------------------------------
#
#
level = {
	'location1' : {
		'description' : '',
		'rooms' : ['location3', 'location2'],
		'items' : [('a bucket','a very old leaky bucket')]
		},
	'location2' : {
		'description' : '',
		'rooms' : ['location3', 'location1'],
		'items' : [('a bucket','a very old leaky bucket')]
		},
	'location3' : {
		'description' : '',
		'rooms' : ['location1', 'location2'],
		'items' : [('a bucket','a very old leaky bucket')]
		}
}


current_location = ''

def goto(location):
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
	goto('location1')

start()
	