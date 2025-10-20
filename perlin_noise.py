import pygame
import random
from PIL import Image,ImageDraw
pygame.init()
w=400
h=400

square_size = (w+h)/4

square_x=(w - square_size)/2
square_y=(h - square_size)/2

win = pygame.display.set_mode((w, h))
pygame.display.set_caption("single square perlin noise")

res=20

pi=3.1416

def generate_grid(resolution=3):
    grid=[]
    width,height=int(square_size/resolution)+1,int(square_size/resolution)+1
    for x in range(width):
        for y in range(height):
            angle=generate_angle()
            vx,vy=generate_unit_vector(angle)
            grid.append([x*resolution,y*resolution,vx,vy,angle])
    return grid

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
    vec_length=30
    pygame.draw.circle(win,(240, 96, 96),(x,y),5)
    pygame.draw.line(win,(96, 168, 240),(x,y),(x+vx*vec_length,y+vy*vec_length),5)

def draw_grid_vectors(grid):
    for cell in grid:
        draw_vector(cell[0]+square_x,cell[1]+square_y,cell[2],cell[3])
# order tl tr bl br
def draw_vectors(dim=(0,0,0,0),vecs=[[0,0]]):
    draw_vector(dim[0],dim[1],vecs[0][0],vecs[0][1])
    draw_vector(dim[2]+dim[0],dim[1],vecs[1][0],vecs[1][1])
    draw_vector(dim[0],dim[3]+dim[1],vecs[2][0],vecs[2][1])
    draw_vector(dim[2]+dim[0],dim[3]+dim[1],vecs[3][0],vecs[3][1])
def softsign(x):
    return x / (1 + abs(x))
def bell(x):
    return 1 / (1 + 20*x * x)

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)
def sigmoid(t):
    return 1 / (1 + pow(2.71828, -t))
def lerp(a, b, t):
    return a + t * (b - a)
def perlin_noise_value(x,y,grid):
    index_tl=int((x/res))+int((y/res))* (int(square_size/res))
    index_tr=index_tl+1
    index_bl=index_tl+(int(square_size/res))
    index_br=index_bl+1
   # print("Indices: ",index_tl,index_tr,index_bl,index_br)
    vecs=[[grid[index_tl][2],grid[index_tl][3]],[grid[index_tr][2],grid[index_tr][3]],[grid[index_bl][2],grid[index_bl][3]],[grid[index_br][2],grid[index_br][3]]]        
    #print("Vectors: ",vecs )

    nx=x%res
    ny=y%res

    #print("Calculating perlin noise for ",nx,ny)

    value=perlin_noise(nx,ny,vecs)
    #print("Perlin value at ",x,y,": ",value)
    return value

def colour_gradient(col1,col2,col3,ratio):
    if ratio<0.5:
        r=int(col1[0]*(1-ratio*2)+col2[0]*(ratio*2))
        g=int(col1[1]*(1-ratio*2)+col2[1]*(ratio*2))
        b=int(col1[2]*(1-ratio*2)+col2[2]*(ratio*2))
    else:
        r=int(col2[0]*(1-(ratio-0.5)*2)+col3[0]*((ratio-0.5)*2))
        g=int(col2[1]*(1-(ratio-0.5)*2)+col3[1]*((ratio-0.5)*2))
        b=int(col2[2]*(1-(ratio-0.5)*2)+col3[2]*((ratio-0.5)*2))
    return (r,g,b)

def perlin_noise(x,y,vecs):
    x=x/res
    y=y/res

    tl=dot(x,y,vecs[0][0],vecs[0][1])
    tr=dot(x-1,y,vecs[1][0],vecs[1][1])


    bl=dot(x,y-1,vecs[2][0],vecs[2][1])
    br=dot(x-1,y-1,vecs[3][0],vecs[3][1])

    # Fade + interpolate
    u = fade(x)
    v = fade(y)
    nx0 = lerp(tl, tr, u)
    nx1 = lerp(bl, br, u)
    nxy = lerp(nx0, nx1, v)

    return bell(nxy)


def draw_perlin_box(x,y,size=50):

    #value=int((perlin_noise(x,y)*127.5+127.5)/10)*10
    value=perlin_noise(x,y)*127.5+127.5
    colour=(value,255-value,value)
    box_x=x+square_x
    box_y=y+square_y

    pygame.draw.rect(win,colour,(box_x,box_y,size,size))

def draw_perlin_grid(grid_size=50):
    width,height=int(square_size/grid_size),int(square_size/grid_size)
    for x in range(width): 
        for y in range(height):
            draw_perlin_box(x*grid_size,y*grid_size,grid_size)

def mix_colours(col1,col2,ratio):
    r=int(col1[0]*ratio+col2[0]*(1-ratio))
    g=int(col1[1]*ratio+col2[1]*(1-ratio))
    b=int(col1[2]*ratio+col2[2]*(1-ratio))
    return (r,g,b)

#draw full perlin noise grid

def draw_full_perlin_grid(grid,resolution=5,bres=5,gen_image=False):
    width,height=int(square_size/resolution),int(square_size/resolution)
    img=Image.new('RGB',(int(square_size),int(square_size)))
    draw=ImageDraw.Draw(img)
   # print(width,height)
    
    for x in range(width*bres): 
        for y in range(height*bres):
            nx=x*resolution/bres
            ny=y*resolution/bres
            #value=int(min(perlin_noise_value(nx,ny,grid)*127.5+127.5,255)/50)*50
            value=min(perlin_noise_value(nx,ny,grid)*127.5+127.5,255)
            #print("Value at ",nx,ny,": ",value)
            
            r=value
            g=value/2
            b=255-value
            colour=mix_colours((r,g,b),(255, 255, 255),0.8)
            colour=colour_gradient((100, 151, 196),(219, 50, 50),(47, 143, 212),value/255)
            box_x=nx+square_x
            box_y=ny+square_y
            pygame.draw.rect(win,colour,(box_x,box_y,int(resolution/bres)+1,int(resolution/bres)+1))
            if gen_image:
                draw.rectangle([int(nx),int(ny),int(nx+resolution/bres)+1,int(ny+resolution/bres)+1],fill=colour)

    if gen_image:
       
        img.save("perlin_noise.png")



run=True
grid=generate_grid(res)
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    win.fill((47, 49, 51))
    pygame.draw.rect(win, (255, 255, 255), (square_x,square_y, square_size, square_size))

    for cell in grid:
        cell[4]+=random.uniform(-0.01,0.1)
        cell[2],cell[3]=generate_unit_vector(cell[4])

    #draw_perlin_grid(1)
    draw_full_perlin_grid(grid,res)
    #draw_grid_vectors(grid)
    


    pygame.display.flip()
