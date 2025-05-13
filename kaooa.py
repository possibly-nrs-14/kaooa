import pygame
pygame.init()
pygame.font.init()
green=(0, 255, 0)
blue=(0, 0, 128)
red=(255,0,0)
yellow=(255,255,0)
purple=(128,0,128)
pink=(255,192,203)
orange=(255, 165, 0)
cyan=(0, 255, 255)
black=(0,0,0)
white=(255,255,255)
crows=7
occupied_crows=[]
captured_crows=0
crow_to_move=""
pairs=[["c1","c2"],["c2","c3"],["c3","c4"],["c1","c5"],["c5","c6"],["c6","c7"],["c7","c8"],["c8","c3"],["c3","c9"],["c9","c2"],["c2","c5"],
       ["c5","c10"],["c4","c8"],["c8","c6"],["c6","c10"]]
circles={"c1": [800,200],"c2": [800,400],"c3": [800,550],"c4": [800,750],"c5": [920,360], "c6": [1010,480],
              "c7": [1130, 640],"c8": [938, 584], "c9": [608, 494],"c10": [1109.73, 297.76]}
vulture_normal_moves={"c1": ["c2","c5"],"c2": ["c1","c3","c5","c9"],"c3": ["c4","c2","c8","c9"],"c4": ["c3","c8"],"c5": ["c1","c2","c6","c10"],
                "c6": ["c7","c8","c5","c10"],"c7": ["c6","c8"],"c8": ["c7","c3","c4","c6"], "c9": ["c2","c3"],"c10": ["c5","c6"]}
crow_moves=vulture_normal_moves
vulture_capture_moves={"c1": {"c3":"c2","c6":"c5"},"c2": {"c4":"c3","c10":"c5"},"c3": {"c1":"c2","c7":"c8"},"c4": {"c2":"c3","c6":"c8"},"c5": {"c7":"c6","c9":"c2"},
                "c6": {"c1":"c5","c4":"c8"},"c7": {"c3":"c8","c5":"c6"},"c8": {"c9":"c3","c10":"c6"}, "c9": {"c5":"c2","c8":"c3"},"c10": {"c2":"c5","c8":"c6"}}
vulture_pos=""
class button:
    def __init__(b, text, FONT, font_size,text_color,back_color,rendered_text,text_object,x,y):
        b.FONT=FONT
        b.font_size=font_size
        b.text_color=text_color
        b.back_color=back_color
        b.text=text
        b.x=x
        b.y=y
        b.rendered_text=rendered_text
        font=pygame.font.Font(b.FONT,b.font_size)
        b.rendered_text=font.render(b.text, True, b.text_color,b.back_color)
        text_object=b.rendered_text.get_rect()
        b.text_object=text_object
        b.text_object.center=(b.x,b.y)
class circle():
    def __init__(c,color,center,radius):
        pygame.sprite.Sprite.__init__(c)
        c.color=color
        c.center=center
        c.radius=radius
        pygame.draw.circle(screen, c.color, c.center, c.radius)
def crow_turn(pick_or_move):
    global crows
    global occupied_crows
    global crow_to_move
    global circles
    global vulture_pos
    global crow_moves
    global vulture_normal_moves
    global vulture_capture_moves
    running=True
    while running:
        mouse=pygame.mouse.get_pos() 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if crows>0: 
                    valid=0
                    for circ in circles.keys():
                        if circles[circ][0]-20<=mouse[0]<=circles[circ][0]+20 and circles[circ][1]-20<=mouse[1]<=circles[circ][1]+20 and circ not in occupied_crows and circ!=vulture_pos:
                            c=circle(black, circles[circ], 20)
                            occupied_crows.append(circ)
                            valid=1
                            break
                    if not valid:
                        continue
                    crows-=1
                    running=False
                else:
                    if pick_or_move=="pick":
                        valid=0
                        for circ in circles.keys():
                            if circles[circ][0]-20<=mouse[0]<=circles[circ][0]+20 and circles[circ][1]-20<=mouse[1]<=circles[circ][1]+20 and circ in occupied_crows and circ!=vulture_pos:
                                crow_to_move=circ
                                valid=1
                                break
                        if not valid:
                            continue
                        running=False
                    elif pick_or_move=="move":
                        valid=0
                        for circ in circles.keys():
                            if circles[circ][0]-20<=mouse[0]<=circles[circ][0]+20 and circles[circ][1]-20<=mouse[1]<=circles[circ][1]+20 and circ not in occupied_crows and circ!=vulture_pos:
                                if circ in crow_moves[crow_to_move]:            
                                    c=circle(cyan, circles[crow_to_move], 20)
                                    C=circle(black, circles[circ], 20)
                                    occupied_crows.remove(crow_to_move)
                                    occupied_crows.append(circ)
                                    valid=1
                                    break
                            elif circles[circ][0]-20<=mouse[0]<=circles[circ][0]+20 and circles[circ][1]-20<=mouse[1]<=circles[circ][1]+20 and circ in occupied_crows and circ!=vulture_pos:
                                crow_to_move=circ
                        if not valid:
                            continue
                        won=1
                        if vulture_pos!="":
                            for c in vulture_normal_moves[vulture_pos]:
                                if c not in occupied_crows:
                                    won=0
                                    break
                            if won:
                                for c in vulture_capture_moves[vulture_pos].keys():
                                    if c not in occupied_crows:
                                        won=0
                                        break
                            if won:
                                screen.blit(crow_win.rendered_text,crow_win.text_object)
                        running=False
        pygame.display.update()
        clock.tick(60) 
def vulture_turn():
    global occupied_crows
    global vulture_pos
    global captured_crows
    global vulture_normal_moves
    global vulture_capture_moves
    running=True
    while running:
        mouse=pygame.mouse.get_pos() 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                quit()
            if event.type==pygame.MOUSEBUTTONDOWN: 
                valid=0
                for circ in circles.keys():
                    if circles[circ][0]-20<=mouse[0]<=circles[circ][0]+20 and circles[circ][1]-20<=mouse[1]<=circles[circ][1]+20 and circ not in occupied_crows:
                        if vulture_pos=="":
                            c=circle(white,circles[circ], 20)
                            vulture_pos=circ
                            valid=1
                            break
                        else:
                            if circ!=vulture_pos:
                                if circ in vulture_normal_moves[vulture_pos]:
                                    c=circle(cyan, circles[vulture_pos], 20)
                                    C=circle(white, circles[circ], 20)   
                                    vulture_pos=circ
                                    valid=1
                                    break
                                elif circ in vulture_capture_moves[vulture_pos]:
                                    if vulture_capture_moves[circ][vulture_pos] in occupied_crows:
                                        captured_crows+=1
                                        c1=circle(cyan, circles[vulture_capture_moves[circ][vulture_pos]], 20)
                                        c2=circle(cyan, circles[vulture_pos], 20)
                                        c3=circle(white, circles[circ], 20)
                                        occupied_crows.remove(vulture_capture_moves[circ][vulture_pos])
                                        vulture_pos=circ
                                        if captured_crows==1:
                                            S=' crow captured'
                                        else:
                                            S=' crows captured'
                                        no_of_captures=button(str(captured_crows)+S,'freesansbold.ttf', 48,pink,purple,"","",1850//2,1800//2)
                                        screen.blit(no_of_captures.rendered_text,no_of_captures.text_object)
                                        if captured_crows==4:
                                            screen.blit(vulture_win.rendered_text,vulture_win.text_object)
                                        valid=1
                                        break
                if not valid:
                    continue
                running=False
        pygame.display.update()
        clock.tick(60) 
def main_game():
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                quit()
        screen.fill("blue")
        for pair in pairs:
            l=pygame.draw.line(screen,red,circles[pair[0]],circles[pair[1]],5)
        for circ in circles.keys():
            c=circle(cyan, circles[circ],20)
        pygame.display.update()
        clock.tick(60) 
        while(True):
            if crows>0:
                crow_turn("")
                vulture_turn()
            else:
                crow_turn("pick")
                crow_turn("move")
                vulture_turn()
def start_game():
    running=True
    while running:
        mouse=pygame.mouse.get_pos() 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type==pygame.MOUSEBUTTONDOWN: 
                if 860<=mouse[0]<=990 and 410<=mouse[1]<=480:
                    main_game()
                    running=False
                    quit()
        screen.fill("red")
        screen.blit(title_button.rendered_text,title_button.text_object)
        screen.blit(play_button.rendered_text,play_button.text_object)
        pygame.display.update()
        clock.tick(60) 
screen=pygame.display.set_mode((1920,1080))
clock=pygame.time.Clock()
title_button=button('kaooa','freesansbold.ttf', 96,green,blue,"","",1860//2,650//2)
play_button=button('play','freesansbold.ttf', 64,green,yellow,"","",1850//2,900//2)
vulture_win=button('The vulture wins!','freesansbold.ttf', 64,green,orange,"","",1850//2,200//2)
crow_win=button('The crows win!','freesansbold.ttf', 64,green,orange,"","",1850//2,200//2)
start_game()
pygame.quit()