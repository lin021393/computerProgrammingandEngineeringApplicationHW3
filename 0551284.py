import configparser
import tkinter as tk
import tkinter.font as tkFont
import math
import re

class Node:
	def __init__(self, x=0, y=0):
		self.x=x
		self.y=y
		self.fill='blue'
	def __str__(self):
		return "(%d, %d)"%(self.x, self.y)

		
		
''' Try, try, and try 
class ParseiniFile:
	def __init__(self, iniFile):
		self.iniFile = iniFile
		
	def calculateData(self):
		config=configparser.ConfigParser()
		config.read(self.iniFile)
		numberOfPoints=config.getint('base', 'points')
		numberOfBars=int(config['base']['bars'])
		E=config.getfloat('base', 'E')

		
'''

		
		
class Member:
	def __init__(self, node0, node1, area=10):
		self.node0=node0
		self.node1=node1
		self.area=area
		self.length=math.sqrt(pow(node0.x-node1.x, 2)+pow(node0.y-node1.y, 2))	#	((node0.x-node1.x)^2+(node0.y-node1.y)^2)^(1/2)
		self.sin=(self.node1.y-self.node0.y)/(self.length)
		self.cos=(self.node1.x-self.node0.x)/(self.length)
	def __str__(self):
		return "(%d, %d) ~ (%d, %d)=%f area: %f"%(self.node0.x, self.node0.y, self.node1.x, self.node1.y, self.length, self.area)
	def getRadius(self):
		if(self.node1.x-self.node0.x==0):
			if(self.node1.y-self.node0.y>0):
				return math.pi/2
			elif(self.node1.y-self.node0.y<0):
				return -math.pi/2
			else: 
				return 0
		else:
			return math.atan((self.node1.y-self.node0.y)/(self.node1.x-self.node0.x))
			
			
class Truss:

	def __init__(self, nodes, members, E=27000):
		self.nodes=nodes
		self.nodeTot=len(nodes)
		self.members=members
		self.memberTot=len(members)
		self.E=E
		
	def showEAL(self):
		for m in range(self.memberTot):
			EAL=self.E*self.members[m].area/self.members[m].length
			print("%d) %.13f"%(m, EAL))
			
	def draw(self):
		self.root=tk.Tk()
		self.myFont=tkFont.Font(family='Arial', size=18)
		self.canvas=tk.Canvas(self.root, bg='#00ff00', width=800, height=600)
		for n in range(len(self.nodes)):
			self.locationTransforming(self.nodes[n])
			self.drawNode(self.nodes[n])
			self.drawFixed(self.nodes[n])
		for p in range(len(self.members)):
			self.drawMember(self.members[p])
		self.canvas.grid(row=0, column=0)
		
	def locationTransforming(self, node):
		node.px=node.x+30
		node.py=500-node.y
		
	def drawNode(self, node):
		self.canvas.create_oval(node.px-5, node.py-5, node.px+5, node.py+5, fill=node.fill, width=1)
		self.canvas.create_text(node.px+15, node.py-15, text=str(node.no), font=self.myFont, fill='black')
		
	def drawMember(self, member):
		self.canvas.create_line(member.node0.px, member.node0.py, member.node1.px, member.node1.py, fill='red', width=member.area)
		x=member.node0.px*0.7+member.node1.px*0.3
		y=member.node0.py*0.7+member.node1.py*0.3
		self.canvas.create_text(x, y, text=str(member.no), font=self.myFont, fill='green')
		
	def drawFixed(self, node):
		if(node.fixedX and node.fixedY):
			self.canvas.create_line(node.px, node.py,
									node.px-15, node.py-15,
									node.px-15, node.py+15,
									node.px, node.py, fill='red', width=3)
		elif(node.fixedX):
			self.canvas.create_oval(node.px-10, node.py, node.px+10, node.py+20, outline='red', width=3)
		else:	print()

###########################################################################################
			
numberOfPoints=0
numberOfBars=0
coordOfX=0
coordOfY=0
nodes=[]
members=[]
data=[]

config=configparser.ConfigParser()
config.read('0551284.ini')

sections=config.sections()

numberOfPoints=config.getint('base', 'points')
numberOfBars=int(config['base']['bars'])
E=config.getfloat('base', 'E')

for i in range(numberOfPoints):
	#data=config['node']["p%d"%i].split(',')
	data=re.split(r'[;,=\s]\s*', config['node']["p%d"%i])
	coordOfX=int(data[0])
	coordOfY=int(data[1])
	nodes.append(Node(coordOfX, coordOfY))
	nodes[i].no=i	#	編號
	print("node: ", i, ":", nodes[i])
	#data=config['node']["fixed%d"%i].split(',')
	data=re.split(r'[;,=\s]\s*', config['node']["fixed%d"%i])
	nodes[i].fixedX=int(data[0])
	nodes[i].fixedY=int(data[1])
	
config.add_section('Out')

for j in range(numberOfBars):
	data=config['member']["bar%d"%j].split(',')
	#data=re.split(r'[;,=\s]\s*', config['node']["fixed%d"%i])
	coordOfX=int(data[0])
	coordOfY=int(data[1])
	area=config.getfloat('member', "area%d"%j)
	members.append(Member(nodes[coordOfX], nodes[coordOfY], area))
	members[j].no=j
	print(members[j], members[j].getRadius(), members[j].sin, members[j].cos)
	config['Out']['sin%d'%j]=str(members[j].sin)	#	one of two different ways to express
	config.set('Out', 'cos%d'%j, str(members[j].cos))	#	one of two different ways to express

#############################################################################################	
	
truss=Truss(nodes, members, E)
truss.showEAL()
truss.draw()

for k in range(numberOfBars):
	config['Out']['EAL%d'%k]=str(truss.E*truss.members[k].area/truss.members[k].length)

config.write(open("0551284Out.ini", "w"), space_around_delimiters=False)