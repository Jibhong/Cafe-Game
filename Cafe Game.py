import pygame
from sys import exit
import random

#region screen
pygame.init()
# screen = pygame.display.set_mode((960, 540))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Café Simmulator")
pygame.display.set_icon(pygame.image.load('graphics/icon.png'))
clock = pygame.time.Clock()
#endregion

#region music
pygame.mixer.init()
pygame.mixer.music.load("audio/music.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(loops=-1)
#endregion

#region cursor
pygame.mouse.set_visible(False)
cursor_surf_idle = pygame.transform.scale(pygame.image.load('graphics/Cursor_idle.png').convert_alpha(), (48, 48))
cursor_surf_active = pygame.transform.scale(pygame.image.load('graphics/cursor_active.png').convert_alpha(), (48, 48))
mouse_state = 0

def UpdateCursor():
    if pygame.mouse.get_focused():
        if mouse_state:
            screen.blit(cursor_surf_active , pygame.mouse.get_pos())
        else:
            screen.blit(cursor_surf_idle , pygame.mouse.get_pos())
    

#endregion

unknown_surface = pygame.image.load('graphics/unknown.png').convert_alpha()

#type[ start of finished[ start_surf[], finished_surf[]]]

customer_surface = [[

            [pygame.transform.scale( pygame.image.load('graphics/customer/start/1/1.png').convert_alpha(), (200, 300))],
            
            [pygame.transform.scale( pygame.image.load('graphics/customer/finished/1.png').convert_alpha(), (200, 300))]],



           [[pygame.transform.scale( pygame.image.load('graphics/customer/start/2/1.png').convert_alpha(), (200, 300)),
             pygame.transform.scale( pygame.image.load('graphics/customer/start/2/2.png').convert_alpha(), (200, 300))],
            
            [pygame.transform.scale( pygame.image.load('graphics/customer/finished/2.png').convert_alpha(), (200, 250))]],



           [[pygame.transform.scale( pygame.image.load('graphics/customer/start/3/1.png').convert_alpha(), (200, 300)),
             pygame.transform.scale( pygame.image.load('graphics/customer/start/3/2.png').convert_alpha(), (200, 300)),
             pygame.transform.scale( pygame.image.load('graphics/customer/start/3/3.png').convert_alpha(), (200, 300))],
            
            [pygame.transform.scale( pygame.image.load('graphics/customer/finished/3.png').convert_alpha(), (300, 300))]],



           [[pygame.transform.scale( pygame.image.load('graphics/customer/seller/s.png').convert_alpha(), (200, 300))],
            
            [pygame.transform.scale( pygame.image.load('graphics/customer/seller/f1.png').convert_alpha(), (300, 300)),
             pygame.transform.scale( pygame.image.load('graphics/customer/seller/f2.png').convert_alpha(), (200, 300))]],



           [[pygame.transform.scale( pygame.image.load('graphics/customer/baby/f.png').convert_alpha(), (200, 300)),
             pygame.transform.scale( pygame.image.load('graphics/customer/baby/f.png').convert_alpha(), (200, 300))],
            
            [pygame.transform.scale( pygame.image.load('graphics/customer/baby/f.png').convert_alpha(), (300, 300))]]]

#type[ state[]]
item_surface = [[pygame.transform.scale( pygame.image.load('graphics/item/orange_juice.png').convert_alpha(), (100, 100))],
                


                [pygame.transform.scale( pygame.image.load('graphics/item/green_tea.png').convert_alpha(), (100, 100))],
                
                

                [pygame.transform.scale( pygame.image.load('graphics/item/bat.png').convert_alpha(), (100, 100))],
                

                
                [pygame.transform.scale( pygame.image.load('graphics/item/money.png').convert_alpha(), (100, 100))],
                

                
                [pygame.transform.scale( pygame.image.load('graphics/item/candy.png').convert_alpha(), (100, 100))],
                
                

                [pygame.transform.scale( pygame.image.load('graphics/item/water.png').convert_alpha(), (100, 100))]]


#region define

def GetFullScreenSurf(image):
    return pygame.transform.scale(pygame.image.load(image), (screen.get_size()))

def FillScreen(image):
    screen.blit(image, (0, 0))

def RenderText (x, y, size, text, color):
    surf = pygame.font.Font('font/MonomaniacOne-Regular.ttf',size).render(text, 1, color)
    rect = surf.get_rect(center = (x, y))
    screen.blit(surf, rect)

def playsound(select, volume = 1):

    match select:

        case 'orange_juice':sound = pygame.mixer.Sound("audio/drink3.mp3")
        case 'green_tea':sound = pygame.mixer.Sound("audio/drink2.mp3")
        case 'water':sound = pygame.mixer.Sound("audio/drink1.mp3")
        case 'bat':sound = pygame.mixer.Sound("audio/bonk.mp3")
        case 'candy':sound = pygame.mixer.Sound("audio/candy.mp3")
        case 'money':sound = pygame.mixer.Sound("audio/money.mp3")

        case 'get_money': sound = pygame.mixer.Sound("audio/cash_out.mp3")

        case 'angry':sound = pygame.mixer.Sound("audio/angry"+str(round(random.random()*2)+1)+".mp3")

        case _:
            print(select)
            return

    sound.set_volume(volume)
    sound.play()

#endregion
#region class

#state 0 = none, 1 = spawned, 2 = angry, 3 = good
class Customer():

    def __init__ (self, position, type):

        self.madded = 0

        self.waiting_bar = [(random.random() * 300) + 300] * 2

        self.surf = pygame.image.load('graphics/unknown.png').convert_alpha()
        self.buying = []
        
        match type:
            case 1:
                self.surf = customer_surface[0][0][0]
                self.buying = ['orange_juice'] * (round(random.random()) + 1)

            case 2:
                self.surf = customer_surface[1][0][round(random.random()*1)]
                self.buying = ['green_tea'] * (round(random.random()) + 1)
                
            case 3:
                self.surf = customer_surface[2][0][round(random.random()*2)]
                self.buying = [*(['orange_juice'] * (round(random.random()) + 1)), *(['green_tea'] * (round(random.random()) + 1)), *(['water'] * (round(random.random())))]

            case 4:
                self.surf = customer_surface[3][0][0]
                self.buying = ['money']

            case 5:
                self.surf = customer_surface[4][0][round(random.random()*1)]
                self.buying = ['candy'] * (round(random.random()) + 1)

        self.pay = 0

        for e in self.buying:
            match e:
                case 'orange_juice':
                    self.pay += 30 + random.random() * 5
                
                case 'green_tea':
                    self.pay += 50 + random.random() * 5
                
                case 'water':
                    self.pay += 20 + random.random() * 5

        self.rect = self.surf.get_rect(midbottom = (screen.get_width() + 300, 600))
        self.position_x = position
        self.state = 1
        self.last_state = 1
        self.type = type
        self.menubox = MenuBox(self.buying, self.rect.center)

    def update_timer(self):

        if self.rect.centerx == self.position_x:
            self.waiting_bar[0] -= 1

        if self.waiting_bar[0] <= 0:
            self.state = 2
            if not self.madded:
                playsound('angry', .5)

                match self.type:

                    case 4:
                        if data[1] > 1000:
                            data[1] /= 100
                        elif data[1] > 200:
                            data[1] = 100 + (random.random()*20) + 5
                        else:
                            data[1] -= 150

                    case 5:
                        data[1] -= 300

                    case _: 
                        data[1] -= 50 + (random.random()*50)

                self.madded = 1

    def animation(self):

        match self.state:
            case 1:
                if self.rect.centerx > self.position_x:
                    self.rect.x -= 10
                else: self.rect.centerx = self.position_x

            case 2:

                if self.rect.centerx > -100:
                    self.rect.x -= 10
                else:
                    self.state = 0

            case 3:

                if self.last_state != 3:

                    self.surf = customer_surface[self.type-1][1][0]
                
                    self.rect = self.surf.get_rect(midbottom = (self.rect.centerx, 600))
                    self.last_state = 3
                    
                    data[1] += (random.random()*10) + 10

                if self.rect.centerx > -100:
                    self.rect.x -= 10
                else:
                    self.state = 0
        self.menubox.update_pos(self.rect.center)

    def money_lost(self, item):
        match item:
            case 'orange_juice':
                data[0] -= 20
            
            case 'green_tea':
                data[0] -= 30

            case 'money':
                data[0] /= 3

            case 'candy':
                data[0] -= 5
            
            case 'water':
                data[0] -= 10

    def get_item(self, item):

        if self.type == 4:
            got_item = 0
            if self.rect.centerx == self.position_x:
                for i in range(len(self.buying)):
                    if not got_item:
                        if item == self.buying[i]:

                            playsound(item)

                            self.buying[self.buying.index(item)] = ''
                            self.menubox.remove_item(item)
                            got_item = 1
                            self.waiting_bar[0] = min(self.waiting_bar[0] + (random.random() * 60) + 60, self.waiting_bar[1])

                            self.money_lost(item)
                            data[1] *= 2
                        
                        elif item == 'bat':

                            playsound(item)

                            got_item = 1
                            self.surf = customer_surface[3][1][1]
                            self.state = 2
                            data[1] -= (random.random()*50)+150

                        if all(e == '' for e in self.buying):
                            self.state = 3

        else:
            got_item = 0
            if self.rect.centerx == self.position_x:
                for i in range(len(self.buying)):
                    if not got_item:
                        if item == self.buying[i]:

                            playsound(item)

                            self.buying[self.buying.index(item)] = ''
                            self.menubox.remove_item(item)
                            got_item = 1
                            self.waiting_bar[0] = min(self.waiting_bar[0] + (random.random() * 60) + 60, self.waiting_bar[1])
                            self.money_lost(item)

                        elif item == 'bat':

                            playsound(item)

                            got_item = 1
                            self.state = 2
                            data[1] -= (random.random()*50)+150

                        if all(e == '' for e in self.buying):
                            if self.type != 5:
                                money.append(Money(self.pay, self.rect.centerx, self.rect.centery + 100))
                            self.state = 3

    def render(self):
        screen.blit(self.surf, self.rect)
        if self.rect.centerx == self.position_x:
            self.menubox.update_timer(self.waiting_bar[0], self.waiting_bar[1])
            self.menubox.render()

#oj, candy, money, bat, green tea, grape juice
class Object():

    def __init__(self, type, position):
        
        self.type = type
        self.position = position
        self.state = 0

        match type:
            case 'orange_juice':
                self.surf = item_surface[0][0]
            
            case 'green_tea':
                self.surf = item_surface[1][0]

            case 'bat':
                self.surf = item_surface[2][0]

            case 'money':
                self.surf = item_surface[3][0]

            case 'candy':
                self.surf = item_surface[4][0]
            
            case 'water':
                self.surf = item_surface[5][0]

        self.rect = self.surf.get_rect(center = (position[0], position[1]))
    
    def item_name(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return self.type
        else:
            return ''

    def pick_item(self):

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.state = 1
            return self
        
    def drop_item(self):
        for e in slot:
            if e.rect.collidepoint(pygame.mouse.get_pos()):
                e.get_item(self.type)
        self.state = 0

    def animation(self):
        if self.state:
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.rect.center = self.position

    def render(self):
        screen.blit(self.surf, self.rect)


class MenuBox():

    def __init__ (self, buying, position):
        
        self.waiting_bar_surf = pygame.transform.scale(pygame.image.load('graphics/mainmenu.jpg').convert(), (180, 10))
        self.waiting_bar_frame_surf = pygame.transform.scale(pygame.image.load('graphics/mainmenu.jpg').convert(), (190, 20))
        self.waiting_bar_surf.fill('Green')
        self.waiting_bar_frame_surf.fill('Black')
        self.waiting_bar_rect = self.waiting_bar_surf.get_rect(center = (position[0], position[1] + 150))
        self.waiting_bar_frame_rect = self.waiting_bar_surf.get_rect(center = (position[0], position[1] + 150))

        self.position = position
        self.surf = []
        self.rect = []
        self.buying = buying

        for i in range(len(buying)):
            size = [100, 100]

            match buying[i]:
                case 'orange_juice':
                    self.surf.append(pygame.transform.scale(item_surface[0][0], (size)))

                case 'green_tea':
                    self.surf.append(pygame.transform.scale(item_surface[1][0], (size)))
                
                case 'money':
                    self.surf.append(pygame.transform.scale(item_surface[3][0], (size)))
                
                case 'candy':
                    self.surf.append(pygame.transform.scale(item_surface[4][0], (size)))

                case 'water':
                    self.surf.append(pygame.transform.scale(item_surface[5][0], (size)))

                case _:
                    self.surf.append(pygame.transform.scale(unknown_surface, (size)))
                    print(buying[i], i)

            self.rect.append(self.surf[i].get_rect(midbottom = (position[0], 800)))

    def update_pos(self, position):
        for i in range(len(self.rect)):
            self.rect[i].centerx = position[0] + 200
            self.rect[i].bottom = position[1] + (i * -100) + 130

            self.waiting_bar_frame_rect.center = [position[0] + 195, position[1] + 140] 
            self.waiting_bar_rect.center = [position[0] + 200, position[1] + 145] 

    def update_timer(self, timer, max):
        self.waiting_bar_surf = pygame.transform.scale(self.waiting_bar_surf, (((timer/max) * 180), 10))
        self.waiting_bar_surf.fill((((-timer/max) + 1)* 255, (timer/max) * 255, 0))

    def remove_item(self, remove):
        
        removed_item = 0
        for i in range(len(self.buying)):
            if removed_item == 0:
                if self.buying[i] == remove:
                    removed_item = 1

    def render(self):
        
        for i in range(len(self.surf)):
            if self.buying[i]:
                screen.blit(self.surf[i], self.rect[i])
            
        screen.blit(self.waiting_bar_frame_surf, self.waiting_bar_frame_rect)
        screen.blit(self.waiting_bar_surf, self.waiting_bar_rect)


class Money():

    def __init__(self, cost, posx, posy):

        self.cost = cost
        
        self.position = [posx + (((random.random()*2)-1)*20), posy + (((random.random()*2)-1)*20)]
        self.surf = pygame.transform.scale(pygame.image.load('graphics/item/money_piece.png').convert_alpha(), (100, 100))
        self.rect = self.surf.get_rect(center = (self.position[0], self.position[1]))
    
    def collect(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            playsound('get_money', .8)
            data[0] += self.cost
            return 1
        return 0

    def render(self):
        screen.blit(self.surf, self.rect)

#endregion

# [money, reputation]
data = [200, 100]
rendering_data = [200, 100]
score = [0, 0]

money = []

game = 0
load_setting = 0
background_surf = ''
holding = ['', '']

while True:

    if load_setting == 0:
        background_surf = GetFullScreenSurf('graphics/mainmenu.png') 
        data = [200, 100]
        rendering_data = [200, 100]
        holding = ['', '']
        money = []
        load_setting = 1

        customer = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 5]
        slot = [    Customer((screen.get_width()/4)*1, random.choice(customer))     ,
                    Customer((screen.get_width()/4)*2, random.choice(customer))     ,
                    Customer((screen.get_width()/4)*3, random.choice(customer))     ]
        
        item = [Object('candy',          [(screen.get_width()/2) - 500, 700]),
                Object('water',          [(screen.get_width()/2) - 300, 700]),
                Object('orange_juice',   [(screen.get_width()/2) - 100, 700]),
                Object('green_tea',      [(screen.get_width()/2) + 100, 700]),
                Object('bat',            [(screen.get_width()/2) + 300, 700]),
                Object('money',          [(screen.get_width()/2) + 500, 700])]

    FillScreen(background_surf)
    RenderText(1400, 900, 100, str(round(score[0] + score[1])), 'White')

    # region start game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            #region game setting

            game = 1
            load_setting = 0

            #endregion

    
    #endregion


    while game == 1:

        if load_setting == 0:
            
            score = [0, 0]
            background_surf = GetFullScreenSurf('graphics/background.jpg')

            load_setting = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game = 0

                # elif event.key == pygame.K_SPACE:
                #     for i in range(3):
                #         slot[i].state = 3
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                picked = 0
                for e in item:
                    if e.item_name() != '' and not picked:
                        holding = [e.item_name(), e.pick_item()]
                        picked = 1

                collected = 0
                for e in money:
                    if e.collect() and not collected:
                        money.remove(e)
                        collected = 1

            elif event.type == pygame.MOUSEBUTTONUP:
                if holding[1]:
                    holding[1].drop_item()
                holding = ['', '']

        #region game engine

            #spawn new customer
        for i in range(3):
            if slot[i].state == 0:
                slot[i] = Customer((i+1) * (screen.get_width()/4), random.choice(customer))

        for e in slot:
            e.update_timer()

        if data[0] <= 0 or data[1] <= 0:
            game = 0

        #endregion

        #region animation

        for e in slot:
            e.animation()

        for e in item:
            e.animation()

        for i in range(len(data)):
            score[i] = max(score[i], data[i])

        #endregion

        #region graphics

        FillScreen(background_surf)

            #render customers
        render_layer_order_setting = [1, 3, 0, 2]
        for i in reversed(render_layer_order_setting):
            for e in slot:
                if e.state == i:
                    e.render()

        for e in item:
            e.render()
        

        for e in reversed(money):
            e.render()

        for i in range(len(data)):
            if rendering_data[i] > round(data[i]):
                rendering_data[i] -= 1
            elif rendering_data[i] < round(data[i]):
                rendering_data[i] += 1

        RenderText(screen.get_size()[0]/2, 150, 100, str(round(rendering_data[0])), 'Black')
        RenderText(screen.get_size()[0]/2, 210, 40, str(round(rendering_data[1])), 'Black')

        if holding[1]:
            holding[1].render()
        #endregion
        

        UpdateCursor()
        pygame.display.update()
        clock.tick(60)

        if game == 0:
            load_setting = 0

    UpdateCursor()
    pygame.display.update()
    clock.tick(60)