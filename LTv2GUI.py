import pygame, random ,time , string
import csv, copy,serial,math
 



#Screen Setup
#screen = pygame.display.set_mode((800,480))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
draw_on = False
drowOn = False
last_pos = (0, 0)
color = (0, 255, 0)
white = (255, 255, 255)
black = (0,0,0)
blue = (0,0,255)
radius = 10

xs=275 #192+(1727-192)/3.0
xl=230 #(1727-192)/3.0
ys=160 #109+(971-109)/5
yl=xl
imgIndex =0
delim = ' '
imageDir = '/home/pi/Documents/LTv2.0/English_Lower_Case/Image'
letterDir = 'English_Lower_Case/Data2/'
lengthOfarr=0
flag=1
#Serial Setup

#time.sleep(8.1)

#serL.write("r\n")
#serR.write("r\n")
#time.sleep(6.1)
def invKin(x_in,y_in):
	#x_in = 0.024+0.052*(1-(xs+xl-x_in)/xl)
	#y_in = 0.1171+0.047*((ys+yl-y_in)/yl)
	R= math.sqrt(x_in**2+y_in**2)
	k=math.atan(y_in/x_in)
	phi=math.acos(R/0.2)

	thetaL=math.degrees(k+phi)
	
	x_in=x_in-0.1	
	
	R= math.sqrt(x_in**2+y_in**2)
	k=math.atan(y_in/x_in)
	phi=math.acos(R/0.2)

	thetaR=math.degrees((k-phi))
	
	return  90.0+thetaR,-90.0+thetaL


def getCoords(xn,yn):
	fx=-0.000191875*xn+0.12770
	#fy= 0.00017125*yn+0.09431875
	fy= 0.000191875*yn+0.087031875
	return fx,fy
	
def roundline(srf, color, start, end, radius=1):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, (x, y), radius)



d = dict.fromkeys(string.ascii_lowercase, [])
letterImg=[]
lettersX = []
lettersY = []

for key in d:
	img = pygame.image.load(imageDir+'/'+key+'.png').convert()
	img = pygame.transform.rotozoom(img,0,4)
	rectImg = img.get_rect()
	rectImg.center = (650, 240)
	letterImg.append(img)
	with open(letterDir+key+'.csv','r') as csvfile:
		coords = csv.reader(csvfile, delimiter=delim)
		#header = next(plots)
		x=[]
		y=[]
		for row in coords:
			x.append(int(xs+20+(xl-30)*float(row[0])))
			y.append(int(ys+20+(yl-30)*float(row[1])))
		lettersX.append(x)
		lettersY.append(y)

		
clear = pygame.image.load('clear.png').convert()
clear=pygame.transform.scale(clear,(50,50))
clear=pygame.transform.rotate(clear,180)
rectClear = clear.get_rect()
rectClear.center = (50, 120)

load = pygame.image.load('load.png').convert()
load=pygame.transform.scale(load,(50,50))
load=pygame.transform.rotate(load,180)
rectLoad = load.get_rect()
rectLoad.center = (50, 180)

startL= pygame.image.load('start.png').convert()
startL=pygame.transform.scale(startL,(50,50))
startL=pygame.transform.rotate(startL,180)
rectStart = startL.get_rect()
rectStart.center = (50, 240)	

closeL= pygame.image.load('exit.png').convert()
closeL=pygame.transform.scale(closeL,(50,50))
#closeL=pygame.transform.rotate(closeL,180)
rectClose = closeL.get_rect()
rectClose.center = (750, 100)	

ResetMs= pygame.image.load('exit.png').convert()
ResetMs=pygame.transform.scale(ResetMs,(50,50))
#closeL=pygame.transform.rotate(closeL,180)
rectResetMs = ResetMs.get_rect()
rectResetMs.center = (750, 200)	

screen.blit(clear,rectClear)
screen.blit(load,rectLoad)
screen.blit(startL,rectStart)	
screen.blit(closeL,rectClose)
screen.blit(ResetMs,rectResetMs)

pygame.draw.circle(screen, color, (int(xs), int(ys)), radius)
pygame.draw.circle(screen, blue, (int(xs+xl), int(ys+yl)), radius)

x=[]
y=[]



try:
    while True:
        rect =pygame.draw.rect(screen,white,(xs,ys,xl,yl),5)
        screen.blit(clear,rectClear)
        screen.blit(load,rectLoad)
        screen.blit(startL,rectStart)
		#screen.blit(closeL,rectClose)
		#screen.blit(ResetMs,rectResetMs)
        for e in pygame.event.get():

			#e = pygame.event.wait()
			#keys=pygame.key.get_pressed()
			if e.type == pygame.QUIT:
				raise StopIteration
			if (e.type == pygame.KEYDOWN):
				if e.key == pygame.K_q:
					raise StopIteration
				if e.key == pygame.K_c:
					screen.fill(black)
			if  e.type == pygame.MOUSEBUTTONDOWN and rectClose.collidepoint(e.pos):
				raise StopIteration
#Reset Motors
			if  e.type == pygame.MOUSEBUTTONDOWN and rectResetMs.collidepoint(e.pos):
				pygame.draw.rect(screen,white,rectResetMs,5)
				pygame.display.flip()
				time.sleep(0.05)
				pygame.draw.rect(screen,black,rectResetMs,5)
				pygame.display.flip()
				#serL.write("r\n")
				time.sleep(3)
				#serR.write("r\n")
				#screen.fill(black)
#Clear check
			if  e.type == pygame.MOUSEBUTTONDOWN and rectClear.collidepoint(e.pos):
				pygame.draw.rect(screen,white,rectClear,5)
				pygame.display.flip()
				pygame.draw.rect(screen,black,rectClear,5)
				time.sleep(0.05)
				drowOn = False
				screen.fill(black)
#Load check 
			if  e.type == pygame.MOUSEBUTTONDOWN and rectLoad.collidepoint(e.pos):
				pygame.draw.rect(screen,white,rectLoad,5)
				pygame.display.flip()
				time.sleep(0.05)
				pygame.draw.rect(screen,black,rectStart,5)
				imgIndex=(imgIndex+1)% len(letterImg)
				screen.blit(letterImg[imgIndex],rectImg)
				pygame.draw.rect(screen,black,rectLoad,5)
				pygame.display.flip()
				pygame.draw.rect(screen,black,(xs,ys,xl,yl))
				rect =pygame.draw.rect(screen,white,(xs,ys,xl,yl),5)
				xp = copy.copy(lettersX[imgIndex])
				yp = copy.copy(lettersY[imgIndex])
				lengthOfarr=len(xp)
				newPoint=pygame.draw.circle(screen, blue, (xp.pop(0),yp.pop(0)), 10)
				flag = 1
				drowOn = False
				drow_on= False
# Start check
			if e.type == pygame.MOUSEBUTTONDOWN and rectStart.collidepoint(e.pos):
				pygame.draw.rect(screen,white,rectStart,5)
				pygame.display.flip()
				time.sleep(0.05)
				pygame.draw.rect(screen,black,(xs,ys,xl,yl))
				rect =pygame.draw.rect(screen,white,(xs,ys,xl,yl),5)
				xp = copy.copy(lettersX[imgIndex])
				yp = copy.copy(lettersY[imgIndex])
				lengthOfarr=len(xp)
				newPoint=pygame.draw.circle(screen, blue, (xp.pop(0),yp.pop(0)), 10)
				pygame.display.flip()
				drowOn = True
				#screen.fill(black)
# Drawing check
			if e.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(e.pos) and drowOn:
				color = (0, 255, 0)
				#pygame.draw.circle(screen, color, e.pos, radius)
				draw_on = True
			if e.type == pygame.MOUSEBUTTONUP:
				draw_on = False
			if  draw_on and e.type == pygame.MOUSEMOTION and rect.collidepoint(e.pos) and newPoint.collidepoint(e.pos):
				#if draw_on and :
					#pygame.draw.circle(screen, color, e.pos, radius)
					#roundline(screen, color, e.pos, last_pos,  radius)
				#last_pos = e.pos
				if lengthOfarr-1>0:
					flag=1
					xp0,yp0=(xp.pop(0),yp.pop(0))
					xc,yc=getCoords(xp0,yp0)
					(thL,thR)=invKin(xc,yc)
					#print 'xp: '+str(xp0)+'yp: '+str(yp0)+'xc: '+str(xc)+'yc: '+str(yc)
					#thL=-90+thL
					#thR=90+thR
					#print str(thL)+' '+str(thR)
					
					sting2send=str(thR)+'\n'
					#serR.write(sting2send)
					
					#readlinR = serR.readline()
					time.sleep(0.002)
					
					sting2send = str(thL)+'\n'
					#serL.write(sting2send)
					time.sleep(0.002)
					readlinL = serL.readline()

					print readlinL,readlinR
					newPoint=pygame.draw.circle(screen, color, (xp0,yp0), 12)
					lengthOfarr-=1
					# TURN ON MAGNET
					#GPIO.output(magnet1Pin,GPIO.LOW)
					#GPIO.output(magnet2Pin,GPIO.HIGH)
					#print("ON")
					#serR.flushInput()
					#serL.flushInput()
					time.sleep(0.02)

					
				else:
					(xin,yin) = getCoords(xs+xl,ys+xl)
					(thL,thR) = invKin(xin,yin)
					#print thL,thR
					#thL = -90+thL
					#thR = 90+thR
					if(flag==1):
						sting2send=str(thR)+'\n'
						#serR.write(sting2send)
						readlinR = serR.readline()
						sting2send = str(thL)+'\n'
						#serL.write(sting2send)
						#readlinL = serL.readline()
						
						print readlinL,readlinR
						draw_on = False
						drawOn = False
						#REVERSE MAGNET POLARITY
						#GPIO.output(magnet1Pin,GPIO.HIGH)
						#GPIO.output(magnet2Pin,GPIO.LOW)
						flag=0
						time.sleep(0.02)
			pygame.display.flip()

except StopIteration:
    pass
string2send=str(0.0)+'\n'
# serL.write(string2send)
# serR.write(string2send)
# time.sleep(0.1)
# serL.close()
# serR.close()

#GPIO.cleanup()

pygame.quit()
