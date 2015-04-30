from random import random
from math import cos,pi,sin
from sys import stdout,argv
from time import sleep

DEG=pi/180
POP=10000
W=640
H=640
verbose=False
screen=False
def draw(screen,points):
	for i in range(-1,len(points)-1):
		x0=int(W/2+scale*points[i][0]*cos(points[i][1]))
		y0=int(H/2-scale*points[i][0]*sin(points[i][1]))
		x1=int(W/2+scale*points[i+1][0]*cos(points[i+1][1]))
		y1=int(H/2-scale*points[i+1][0]*sin(points[i+1][1]))
		screen.linea((x0,y0),(x1,y1))
	for p in points:
		x=int(W/2+scale*p[0]*cos(p[1]))
		y=int(H/2-scale*p[0]*sin(p[1]))
		screen.punto(x,y,VERDE)
def R(a,e,phi,theta):
	try:
		return a*(1-e**2)/(1-e*cos(theta-phi))
	except:
		return 0

def SEC(vector):
	a,e,phi=vector
	sec=0
	for r,theta in points:
		rr=R(a,e,phi,theta)
		if verbose:
			print "theta=%.2f\tR=%.2f\tr=%.2f"%(theta,rr,r)
		sec+=(rr-r)**2
	return sec

def eval(vector):
	return poplensq/(1.0+SEC(vector[0],vector[1],vector[2]))

def mutate(father,n):
	if n>1000 and n<2000:
#	rand=random()
#	if rand<0.3:
		return [father[0]*(1+.05*(random()-0.5)),father[1],father[2]]
	elif n>=2000 and n<3000:
		return [father[0],max(0,min(1,father[1]+.2*(random()-0.5))),father[2]]
	elif n>=3000 and n<4000:
		return [father[0],father[1],father[2]+random()-0.5]
	else:
		return [father[0]*(1+0.2*(random()-0.5)),
			max(0,min(1,father[1]+.2*(random()-0.5))),#0.1*father[1]*(random()-0.5),
			father[2]+.1*(random()-0.5)]#0.1*father[2]*(random()-0.5)]

if '-h' in argv:
	print "Fitting an ellipse to a set of points with a genetic algorithm"
	print ""
	print "Usage: %s <options>"
	print "Then introduce set of points r,theta"
	print ""
	print "-h\tThis help"
	print "-v\tVerbose"
	print "-g\tShow graphic fitting"
	exit()
verbose='-v' in argv
screen='-g' in argv
## Get points
points = []
while 1:
	try:
		points.append(map(float,input()))
	except:
		break
poplensq=len(points)**2
## Initial guess
print "Guessing initial values"
sol=[0,0,0]
rs=map(lambda x:x[0],points)
sol[0]=sum(rs)/len(rs)
del rs
sol[1]=1-min(points)[0]/max(points)[0]
sol[2]=max(points)[1]
print "Starting with",sol
print "Generating first population (%d individuals)"%POP
pop=[sol]
solev=SEC(sol)
for p in range(POP):
	pop.append([(.5+random())*sol[0],random(),random()*2*pi])
for i in pop:
	seci=SEC(i)
	if seci<solev:
		sol=i
		solev=seci
del(seci)
del(pop)
print "Beginning evolution"
## Begin evolution
ev=1000000000000000
g=0
if screen:
	from graf import *
	maxval=max(points)[0]
	scale=300./maxval
	scrn=Pantalla(W,H)
	scrn.fondo()
	for th in range(360):
		r=R(sol[0],sol[1],sol[2],th*DEG)
		x=int(W/2+scale*r*cos(th*DEG))
		y=int(H/2-scale*r*sin(th*DEG))
		scrn.punto(x,y,AZUL)
	draw(scrn,points)
	scrn.actualizar()
while ev>.1:#10000./len(points):
	n=0
	solev=SEC(sol)/poplensq
	if verbose:
		print solev
	while ev>.98*solev:
		son=mutate(sol,n)
		n+=1
		ev=SEC(son)/poplensq
	sol=son
	if g%1==0:
		print "-----"
		print "Gen %d, Children %d, SEC=%.2f"%(g,n,ev)
		print sol
		if screen:
			scrn.fondo()
			for th in range(360):
				r=R(sol[0],sol[1],sol[2],th*DEG)
				x=int(W/2+scale*r*cos(th*DEG))
				y=int(H/2-scale*r*sin(th*DEG))
				scrn.punto(x,y,ROJO)
			draw(scrn,points)
			scrn.actualizar()
			sleep(.5)

	g+=1
print "\nSolution:gen %d,%.2fv"%(g,ev),sol
if screen:
	while 1:
		scrn.endloop()
		sleep(.1)
