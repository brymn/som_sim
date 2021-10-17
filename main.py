import pygame
import names
import random

pygame.init()
clock = pygame.time.Clock()
fps = 60

WIDTH = 960
HEIGHT = 720
STEP = 20
HALF_STEP = STEP/2

BLACK = (0,0,0)
WHITE = (255,255,255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SOM_SIM")
pygame.font.init()
myfont = pygame.font.SysFont('Roboto-Medium.ttf', STEP)


current_volume = 0
final_volume = 10000

unload_pending_trailers = [] #|better as a list or better as a sprite group?
unloading_trailers = []


# in progress, needs update function associated with the assigned unloader to decrease package count and signal that it is ready for a trailer switch when empty
#future: display count of packages remaining and update image to reflect empty when package count == 0
 
class Trailer: 
    def __init__(self, id_number, volume):
        self.id_number = id_number
        self.volume = volume

employee_group = pygame.sprite.Group()


class Employee(pygame.sprite.Sprite):
    def __init__(self, name, id_number, assignment):
        super().__init__()
        self.name = name
        self.id_number = id_number
        self.assignment = assignment #assignment will be used to position the employee 
        self.rate_modifier = (round(random.uniform(0.85, 1.15), 2))
        self.next_package = 0 
        self.image = pygame.image.load('graphics/worker_stand.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (STEP*2, STEP*2))
        self.rect = self.image.get_rect()

#needs behavior for detecting collisions with boxes assigned to vans matching the van assignments, going to the appropriate van, turning, and reseting. 
#looping movement to demonstrate uninteligent example
class Loader(Employee):
    def __init__(self, name, id_number, assignment, set):
        super().__init__(name, id_number, assignment)
        self.standard_load_rate = 3000
        self.load_efficiency = self.rate_modifier * self.standard_load_rate
        self.set = set
        self.rect.x = (4 * STEP) + ((STEP)*(assignment * 3)) - (HALF_STEP)
        self.rect.top = 16 * STEP + ((set * 9))*STEP
        if self.assignment % 2 != 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.walk_speed = 2
        self.walk_direction = 1
        self.walk_count = 1

#arbitrary demonstration of movement
    def update(self):
        if self.walk_count % 60 != 0:
            self.rect.y += (self.walk_speed * self.walk_direction)
            self.walk_count += 1
        else:
            self.walk_direction *= -1 
            self.walk_count += 1
            self.image = pygame.transform.flip(self.image, True, False)
        

#complete, for now | simple.
#in the future will be interactable to change trailer assignments to speed up/slow down certian trailers
class Unloader(Employee): 
    def __init__(self, name, id_number, assignment):
        super().__init__(name, id_number, assignment)
        self.standard_unload_rate = 3500
        self.unload_efficiency = self.rate_modifier * self.standard_unload_rate

    def update(self):
        global current_volume
        time_now = pygame.time.get_ticks()
        if time_now >= self.next_package:
            new_package = Package(self.assignment)
            package_group.add(new_package)
            self.next_package = time_now + self.unload_efficiency
            current_volume += 1


van_group = pygame.sprite.Group()

# have not started this yet. After progress is made on 'Loader'
class Van(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('graphics/truck_butt_left.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (STEP-1, STEP*2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.volume = 0
        
    def update(self):
        pass


package_group = pygame.sprite.Group()

class Package(pygame.sprite.Sprite):#needs a van assignment in addition to van line and a method to .kill() when collides with a loader assigned to that same van
    def __init__(self,origin_door):
        super().__init__()
        self.image = pygame.image.load('graphics/brooks_box.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, ((STEP), STEP))
        self.rect = self.image.get_rect()
        self.origin_door = origin_door
        self.sort_position = (self.origin_door * STEP)+ (8 * STEP)
        self.destination_belt = random.randint(1,7)
        self.destination_belt_x = (self.destination_belt*6)*STEP-(HALF_STEP)
        self.rect.left = ((origin_door*6)*STEP)-(HALF_STEP)
        self.rect.top = 6*STEP

    def update(self):
        if self.rect.top < self.sort_position:
            self.rect.y += 1
        elif self.rect.top == self.sort_position:
            if self.rect.left < self.destination_belt_x:
                self.rect.x += 1
            if self.rect.left > self.destination_belt_x:
                self.rect.x -= 1
            if self.rect.left == self.destination_belt_x:
                self.rect.y += 1
        if self.rect.top > self.sort_position:
            self.rect.y += 1       
        if self.rect.bottom > ((HEIGHT-STEP)):
            self.kill()
        

def initialize_trailer():
    trailer_id_number = str(random.randint(800000,899999))
    volume = random.randint(750,1200)
    new_trailer = Trailer(trailer_id_number, volume)
    unload_pending_trailers.append(new_trailer)

def populate_loaders():
    for i in range(0,14):
        for j in range(0,2):
            employee_name = names.get_full_name()
            employee_id_number = str(random.randint(200000,399999))
            new_loader = Loader(employee_name, employee_id_number, i,j)
            employee_group.add(new_loader)


#arbitrary for now
def populate_yard(count):
    for i in range(count):
        initialize_trailer()

#auto-assigned for now. Will be interactive in the future. 
def populate_unload(doors):
    for trailer in range(doors):
        employee_name = names.get_full_name()
        employee_id_number = str(random.randint(200000,399999))
        new_unloader = Unloader(employee_name, employee_id_number, trailer+1)
        employee_group.add(new_unloader)
        next_trailer = unload_pending_trailers.pop(trailer)
        unloading_trailers.append(next_trailer)

#runs the group initializations as a single function to be called below
def initialize_all_objects():
    populate_yard(40)
    populate_unload(7)
    populate_loaders()

initialize_all_objects()

#these were used to generate the background image, but was causing the game to run very slowly...
#so a screenshot was taken and is used as the base layer. Thse functions will be kept for when the images
#get upgraded and need updating. The screenshot method will likely be done again. Pygame can't handle that many blits
def draw_floor():
    for i in range(int(WIDTH/STEP)):
        for j in range(int(HEIGHT/STEP)):
            image = pygame.image.load('graphics/ground_tile.png').convert_alpha()
            screen.blit(image,(i*STEP, j*STEP))

def draw_vanlines():
    for i in range(5,43,6):
        image = pygame.image.load('graphics/belt_conveyor.png').convert_alpha()
        image = pygame.transform.scale(image, (STEP*2, STEP*30))
        screen.blit(image, (i*STEP, 5*STEP))
 
def draw_sorter():
    for i in range(9,16):
        image = pygame.image.load('graphics/belt_conveyor_horizontal.png').convert_alpha()
        image = pygame.transform.scale(image, (STEP*38, STEP))
        screen.blit(image, (5*STEP, i*STEP))

def draw_trailer():
    for i in range(4, 43, 6):
        image = pygame.image.load('graphics/trailer_loaded.png').convert_alpha()
        image = pygame.transform.scale(image, (STEP*4, STEP*4))
        screen.blit(image,(i*STEP, 1*STEP))

def draw_walk_area():
    image = pygame.image.load('graphics/dock_walk_surface.png').convert_alpha()
    image = pygame.transform.scale(image,(STEP, STEP*19))
    for i in range(4,45,3):
        screen.blit(image, (i*STEP, 16*STEP))


def draw_static_background():
    image = pygame.image.load('graphics/static_background2.png').convert_alpha()
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    screen.blit(image, (0,0))

#made after the base layer was snipped. Will be integrated in the future and not drawn each time. 
def make_vans():
    for i in range(3,40,6):
        for k in range(8,45,6):
            for j in range(18, 34, 3):
                new_van = Van(i * STEP, j * STEP)
                new_van_1 = Van(k * STEP, j * STEP)
                van_group.add(new_van)
                van_group.add(new_van_1) # second group w/ adjustment to be placed on the other side of the van line

make_vans()


text_box = pygame.Rect(HALF_STEP, (STEP*5)+HALF_STEP, STEP*4, STEP*10)

def create_timer_text():
    timer_text = myfont.render('TIME', True, WHITE, None)
    return timer_text

#quick and easy. Will need to fix later. Game is not inteded to run for > 1 hour...
def update_timer():
    seconds = int((pygame.time.get_ticks()/1000))
    hours = int(seconds / 3600)
    minutes = int(seconds / 60)
    seconds = int(seconds % 60)

    elapsed_time = myfont.render(str(hours) + ":" + str(minutes) + ":" + str(seconds), True, WHITE, None)
    return elapsed_time

def create_tput_text():
    tput_text = myfont.render('THRUPUT', True, WHITE, None)
    return tput_text

def update_tput():
    time = round((pygame.time.get_ticks()/1000),0)
    tput_calc = int((current_volume/time) * 3600)
    tput_perhour = myfont.render(str(tput_calc), True, WHITE , None)
    return tput_perhour

def create_volume_text():
    volume_text = myfont.render('VOLUME', True, WHITE, None)
    return volume_text

def update_volume():
    volume = myfont.render(str(current_volume) + "/" + str(final_volume), True, WHITE, None)
    return volume 

def draw_background():
    draw_static_background()
    #draw_floor()
    #draw_vanlines()
    #draw_sorter()
    #draw_trailer()
    #draw_worker()
    #draw_walk_area()



running = True
while running:

    clock.tick(fps)
    timer = create_timer_text()
    time = update_timer()
    tput_text = create_tput_text()
    tput = update_tput()
    volume_text = create_volume_text()
    volume = update_volume()

    if current_volume >= final_volume:
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False      

    draw_background()
    van_group.draw(screen)
    package_group.draw(screen)
    package_group.update()
    employee_group.update()
    employee_group.draw(screen)

    pygame.draw.rect(screen, BLACK, text_box)
    screen.blit(timer, (STEP, STEP*6))
    screen.blit(time, (STEP, STEP*7))
    screen.blit(volume_text, (STEP, STEP*8))
    screen.blit(volume, (STEP, STEP*9))
    screen.blit(tput_text, (STEP, STEP*10))
    screen.blit(tput, (STEP, STEP*11))
    pygame.display.update()
