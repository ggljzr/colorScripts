import sys
import os
import argparse
from termcolor import colored
from random import randint

#terminal size
rows, columns = os.popen('stty size', 'r').read().split()

boxChar = u'\u2588'

#command line arguments
parser = argparse.ArgumentParser(description='Simple script for displaying terminal colors. For Python2.7')

parser.add_argument('--terminal','-t',  required=False,
                    action='store_true',help='Use terminal size, approximately. Works better in vertical mode')

parser.add_argument('--values','-v',required=False,action='store_true',
		    help='Print color values, overrides other options except --box')

parser.add_argument('--text','-tx',required=False, action='store_true',
		    help='Print colored text on colored background to test visibility')

parser.add_argument('--grey', '-g', required=False, action='store_true',
		   help='Include grey in color print')

parser.add_argument('--box', '-b', required=False, action='store_true',
		    help='Uses box ' + u'\u25a0' + ' instead of rectangle')

parser.add_argument('--style', '-s', required=False,
                    default='normal',
                    choices=['normal','bold','both'],
                    type=str, help='choose color style (normal, bold or both)')


parser.add_argument('--direction', '-d',  
		    required=False, default='vertical', 
	            choices=['horizontal','vertical', 'random'],type=str, 
                    help='choose direciton of print (horizontal, vertical or random)')


parser.add_argument('--width', '-W', 
		    required=False, default='20', type=int, help='Width, default 20',)

parser.add_argument('--height', '-H',
                    required=False, default='20', type=int,  help='Height, default 20')

#function to print colors in lines verticaly
def printVertical(height, width, style, colors):
	colorWidth = width / len(colors)
	for i in range (0, height):
		for color in colors:
			if style == 'both':
				box =  colored(boxChar*(colorWidth/2),color , attrs=[])
				sys.stdout.write(box)
				box =  colored(boxChar*(colorWidth/2),color , attrs=['bold'])
				sys.stdout.write(box)
			else:
				box =  colored(boxChar*(colorWidth),color , attrs=[style])
				sys.stdout.write(box)
		print ''

#function to print colors in lines horizontaly
def printHorizontal(height,width, style,colors):
	colorHeight = height / len(colors)
	boxStyle = [style]
	if style == 'both':
		boxStyle = []
		colorHeight = colorHeight / 2
	for color in colors:
		box = colored(boxChar*width, color, attrs=boxStyle)
		boldBox = colored(boxChar*width, color, attrs=['bold'])
		for j in range(0, colorHeight):
			print box
		if style == 'both':
			for k in range(0,colorHeight):
				print boldBox

def printRandom(height, width, style, colors):
	lStyle = style
	for i in range(0, height):
		for j in range(0, width):
			if style == 'both':
				randStyle = randint(0,1)
				if randStyle == 1:
					lStyle = 'bold'
				else:
					lStyle = 'underline'		
			rand = randint(0,len(colors) - 1)
			box = colored(boxChar, colors[rand],attrs=[lStyle])
			sys.stdout.write(box)
		print ''
	
def colorValues(colors):
	Xresources = os.popen('xrdb -query','r')
	colorValues = []	
	colorNum = len(colors)

	for l in Xresources:
		if '*color' in l:
			l = l.replace("\t","")
			color, value = l.split(':')
			value = value.replace("\n","")
			colorValues.append([color,value])
	for i in colorValues:
		i[0] = i[0].replace("*color","")
		i[0] = int(i[0])

	colorValues = sorted(colorValues, key = lambda color: color[0])
	
	colorPointer = 0
	for i in colorValues:
		i.append(colors[colorPointer])
		colorPointer = (colorPointer + 1) % colorNum		

	style = []
	printStyle = 'normal'
	for i in colorValues:
		if i[0] > 7:
			style = ['bold']
			printStyle = 'bold'

		box = colored(boxChar*3, i[2],attrs=style)
		sys.stdout.write(box)
		print ' - ' + i[2] + ' ' + printStyle  + ' (' + i[1] + ')' 

def textOutput(colors):
	print '------------------------------------------------------'
	for background in colors:
		bckg = 'on_' + background
		for foreground in colors:
			output = colored(' ' + foreground + ' ', foreground, bckg)
			sys.stdout.write(output)
		print ''
		for foreground in colors:
			output = colored(' ' + foreground + ' ', foreground, bckg, attrs=['bold'])
			sys.stdout.write(output)
		print ''
	print '------------------------------------------------------'


if __name__ == '__main__':
	
	colors = ['grey','red','green','blue','cyan','yellow','magenta','white']

	args = parser.parse_args()

	style = args.style

	if args.box == True:
		boxChar = u'\u25a0'

	if args.values == True:
		colorValues(colors)
	
	elif args.text == True:
		textOutput(colors)
	else:
		if args.grey == False:
			colors.remove('grey')
			colors.remove('white')

		if style == 'normal':
			style = 'underline' #workaround

		if args.terminal == True:
			width = int(columns)
			height = int(rows) 
		else:
			width = args.width
			height = args.height

		if(args.direction == 'vertical'):
			printVertical(height, width, style, colors)
		elif(args.direction == 'horizontal'):
			printHorizontal(height, width, style, colors)
		elif(args.direction == 'random'):
			printRandom(height,width, style, colors)			
