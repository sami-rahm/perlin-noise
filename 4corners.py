import pygame
import random

pygame.init()
w=500
h=500

square_size = (w+h)/4

square_x=(w - square_size)/2
square_y=(h - square_size)/2

win = pygame.display.set_mode((w, h))
pygame.display.set_caption("single square perlin noise")

pi=3.1416

def dot(x1,y1,x2,y2):
    return x1*x2+y1*y2

def qsin(theta):   
    if theta==0:
        return 0  
    n=theta%pi
    x=pi-n
    ans= 16*n*x/(5*pi*pi-4*n*x)
    if (theta//pi)%2==0:
        return ans
    else:
        return -ans
def qcos(theta):
    return qsin(theta+pi/2)

def generate_angle():
    return random.random()*2*pi

def generate_unit_vector(angle):
    return qcos(angle), qsin(angle)

  

def draw_vector(x,y,vx,vy):
    vec_length=100
    pygame.draw.circle(win,(240, 96, 96),(x,y),10)
    pygame.draw.line(win,(96, 168, 240),(x,y),(x+vx*vec_length,y+vy*vec_length),10)
    
# order tl tr bl br
def draw_vectors(dim=(0,0,0,0),vecs=[[0,0]]):
    draw_vector(dim[0],dim[1],vecs[0][0],vecs[0][1])
    draw_vector(dim[2]+dim[0],dim[1],vecs[1][0],vecs[1][1])
    draw_vector(dim[0],dim[3]+dim[1],vecs[2][0],vecs[2][1])
    draw_vector(dim[2]+dim[0],dim[3]+dim[1],vecs[3][0],vecs[3][1])




vecs=[generate_unit_vector(generate_angle()) for _ in range(4)]

def perlin_noise(x,y):
    x=x/square_size
    y=y/square_size

    tl=dot(x,y,vecs[0][0],vecs[0][1])
    tr=dot(x,y,vecs[1][0],vecs[1][1])

    interpolated_top=tl*(x/square_size)+tr*(1 - x/square_size)

    bl=dot(x,y,vecs[2][0],vecs[2][1])
    br=dot(x,y,vecs[3][0],vecs[3][1])

    interpolated_bottom=bl*(x/square_size)+br*(1 - x/square_size)

    final_value=interpolated_top*(y/square_size)+interpolated_bottom*(1 - y/square_size)
    value2=(tl+tr+bl+br)/4

    return value2
def sigmoid(x):
    return 1/(1+2.71828**(-x))

def draw_perlin_box(x,y,size=50):

    #value=int((perlin_noise(x,y)*127.5+127.5)/10)*10
    value=perlin_noise(x,y)*127.5+127.5
    colour=(value,value,value)
    box_x=x+square_x
    box_y=y+square_y

    pygame.draw.rect(win,colour,(box_x,box_y,size,size))

def draw_perlin_grid(grid_size=50):
    width,height=int(square_size/grid_size),int(square_size/grid_size)
    for x in range(width): 
        for y in range(height):
            draw_perlin_box(x*grid_size,y*grid_size,grid_size)




run=True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    win.fill((47, 49, 51))
    pygame.draw.rect(win, (255, 255, 255), (square_x,square_y, square_size, square_size))

    draw_perlin_grid(25)

    draw_vectors((square_x,square_y,square_size,square_size),vecs)


    pygame.display.flip()
