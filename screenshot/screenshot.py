import pygame, sys, os
from pygame.locals import K_a, K_s,K_w,K_d,K_LEFTBRACKET,K_RIGHTBRACKET
from PIL import Image
pygame.init()

BG_COLOR = (0,0,0)


def screenshot_active(filename):
    # use xdotool to find the id of active window
    os.system('import -window "$(xdotool getwindowfocus -f)" {}'.format(filename))

def screenshot_region(filename):
    input_loc = 'stack.png'
    os.system('import -window root {}'.format(input_loc))
    screen, px = setup(input_loc)
    left, upper, right, lower = mainLoop(screen, px)

    # ensure output rect always has positive width, height
    if right < left:
        left, right = right, left
    if lower < upper:
        lower, upper = upper, lower
    im = Image.open(input_loc)
    im = im.crop(( left, upper, right, lower))
    pygame.display.quit()
    im.save(filename)

def displayImage(screen, px, topleft, prior, pos, scale):
    # ensure that the rect always has positive width, height
    topleft = [(val/scale-pos[i]) for i,val in enumerate(topleft)]
    x, y = topleft
    width =  pygame.mouse.get_pos()[0] - topleft[0]
    height = pygame.mouse.get_pos()[1] - topleft[1]
    if width < 0:
        x += width
        width = abs(width)
    if height < 0:
        y += height
        height = abs(height)

    # eliminate redundant drawing cycles (when mouse isn't moving)
    current = x, y, width, height
    if not (width and height):
        return current
    if current == prior:
        return current

    # draw transparent box and blit it onto canvas
    rect = px.get_rect()
    px = pygame.transform.scale(px,[int(rect.width/scale), int(rect.height/scale)])
    screen.blit(px, px.get_rect())
    im = pygame.Surface((width, height))
    im.fill((128, 128, 128))
    pygame.draw.rect(im, (32, 32, 32), im.get_rect(), 1)
    im.set_alpha(128)
    screen.blit(im, (x, y))
    pygame.display.flip()

    # return current box extents
    return (x, y, width, height)

def setup(path):
    px = pygame.image.load(path)
    screen = pygame.display.set_mode((px.get_rect().width, px.get_rect().height))
    screen.blit(px, px.get_rect())
    pygame.display.flip()
    return screen, px

def move(pos,scale,px,screen):
    x,y = pos
    rect = px.get_rect()
    screen.fill(BG_COLOR)
    px = pygame.transform.scale(px,[int(rect.width/scale), int(rect.height/scale)])
    screen.blit(px, (rect[0]-x,rect[1]-y))
    pygame.display.flip()

def mainLoop(screen, px):
    topleft = bottomright = prior = None
    n=0
    scale = 1
    pos = [0,0]
    while n!=1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if not topleft:
                    topleft = [(val+pos[i])*scale for i,val in enumerate(event.pos)]
                    move(pos,scale,px,screen)
                else:
                    bottomright = [(val+pos[i])*scale for i,val in enumerate(event.pos)]
                    move(pos,scale,px,screen)
                    n=1

            if event.type == pygame.KEYDOWN and event.key == K_a:
                pos = [pos[0]-200,pos[1]]
                move(pos,scale,px,screen)
            if event.type == pygame.KEYDOWN and event.key == K_d:
                pos = [pos[0]+200,pos[1]]
                move(pos,scale,px,screen)
            if event.type == pygame.KEYDOWN and event.key == K_w:
                pos = [pos[0],pos[1]-200]
                move(pos,scale,px,screen)
            if event.type == pygame.KEYDOWN and event.key == K_s:
                pos = [pos[0],pos[1]+200]
                move(pos,scale,px,screen)
            if event.type == pygame.KEYDOWN and event.key == K_RIGHTBRACKET:
                scale = scale/1.25
                move(pos,scale,px,screen)
            if event.type == pygame.KEYDOWN and event.key == K_LEFTBRACKET:
                scale = scale*1.25
                move(pos,scale,px,screen)
        if topleft:
            prior = displayImage(screen, px, topleft, prior, pos, scale)
    return ( topleft + bottomright )
