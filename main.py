import pygame
import names
import random

#initializes the pygame
pygame.init()
clock = pygame.time.Clock()
fps = 60

WIDTH = 960
HEIGHT = 720
SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SOM_SIM")

#sort wide variables | there is a better way to organize and declare these
#will need to be declared as global in the unload function - not preferred?
current_volume = 0
final_volume = 100

unload_pending_trailers = []
unloading_trailers = []

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
        self.assignment = assignment 
        self.rate_modifier = (round(random.uniform(0.5, 1.2), 2))
        self.next_package = 0
        self.image = pygame.image.load('graphics/worker_stand.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE*3, SIZE*6))
        self.rect = self.image.get_rect()
        self.rect.center = (100,100)


class Loader(Employee):
    def __init__(self, name, id_number, assignment, set):
        super().__init__(name, id_number, assignment)
        self.load_efficiency = self.rate_modifier * 6000
        self.set = set
        self.rect.left = (assignment*SIZE)
        self.rect.top = (set*10)*SIZE

    def update(self):
        pass


class Unloader(Employee):
    def __init__(self, name, id_number, assignment):
        super().__init__(name, id_number, assignment)
        self.unload_efficiency = self.rate_modifier * 3000

    def update(self):
        global current_volume
        time_now = pygame.time.get_ticks()
        if time_now >= self.next_package:
            new_package = Package(self.assignment)
            package_group.add(new_package)
            self.next_package = time_now + self.unload_efficiency
            current_volume += 1

van_group = pygame.sprite.Group()

class Van(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('graphics/truck_butt_left.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE-1, SIZE*2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        pass


package_group = pygame.sprite.Group()

class Package(pygame.sprite.Sprite):
    def __init__(self,origin_door):
        super().__init__()
        self.image = pygame.image.load('graphics/brooks_box.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, ((SIZE), SIZE))
        self.rect = self.image.get_rect()
        self.origin_door = origin_door
        self.sort_position = (self.origin_door * SIZE)+ (8 * SIZE)
        self.destination_belt = random.randint(1,7)
        self.destination_belt_x = (self.destination_belt*6)*SIZE-(SIZE/2)
        self.rect.left = ((origin_door*6)*SIZE)-(SIZE/2)
        self.rect.top = 6*SIZE

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
        if self.rect.bottom > ((HEIGHT-SIZE)):
            self.kill()
        
#initialization functions for individual classes
def initialize_trailer():
    trailer_id_number = str(random.randint(800000,899999))
    volume = random.randint(750,1200)
    new_trailer = Trailer(trailer_id_number, volume)
    unload_pending_trailers.append(new_trailer)

def test_loaders():
    for i in range(3,45,3):
        employee_name = names.get_full_name()
        employee_id_number = str(random.randint(200000,399999))
        new_loader = Loader(employee_name, employee_id_number, i,1)
        employee_group.add(new_loader)

#test_loaders()

def populate_yard(count):
    for i in range(count):
        initialize_trailer()

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

initialize_all_objects()

#these were used to generate the background image, but was causing the game to slow down
#so a screenshot was taken and is used. Thse functions will be kept for when the images
#get upgraded and need 
def draw_floor():
    for i in range(int(WIDTH/SIZE)):
        for j in range(int(HEIGHT/SIZE)):
            image = pygame.image.load('graphics/ground_tile.png').convert_alpha()
            screen.blit(image,(i*SIZE, j*SIZE))

def draw_vanlines():
    for i in range(5,43,6):
        image = pygame.image.load('graphics/belt_conveyor.png').convert_alpha()
        image = pygame.transform.scale(image, (SIZE*2, SIZE*30))
        screen.blit(image, (i*SIZE, 5*SIZE))
 
def draw_sorter():
    for i in range(9,16):
        image = pygame.image.load('graphics/belt_conveyor_horizontal.png').convert_alpha()
        image = pygame.transform.scale(image, (SIZE*38, SIZE))
        screen.blit(image, (5*SIZE, i*SIZE))

def draw_trailer():
    for i in range(4, 43, 6):
        image = pygame.image.load('graphics/trailer_loaded.png').convert_alpha()
        image = pygame.transform.scale(image, (SIZE*4, SIZE*4))
        screen.blit(image,(i*SIZE, 1*SIZE))
    
def draw_static_background():
    image = pygame.image.load('graphics/static_background2.png').convert_alpha()
    image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    screen.blit(image, (0,0))

def make_vans():
    for i in range(3,40,6):
        for k in range(8,45,6):
            for j in range(18, 34, 3):
                new_van = Van(i * SIZE, j * SIZE)
                new_van_1 = Van(k * SIZE, j * SIZE)
                van_group.add(new_van)
                van_group.add(new_van_1) # second group w/ adjustment to be placed on the other side of the van line

make_vans()

def draw_walk_area():
    image = pygame.image.load('graphics/dock_walk_surface.png').convert_alpha()
    image = pygame.transform.scale(image,(SIZE, SIZE*19))
    for i in range(4,45,3):
        screen.blit(image, (i*SIZE, 16*SIZE))

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
    #employee_group.draw(screen)

    pygame.display.update()
