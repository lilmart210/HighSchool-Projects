import pygame
import math
import numpy as np
import random

#from pygame.locals import *
#import sys; sys.path.insert(0, "..")
#from pgu import gui

#don't think i need to import sys
pygame.init()

with_edge_offset = 400
actual_width = 1000 + with_edge_offset
width = actual_width - with_edge_offset
height = 500
screen = pygame.display.set_mode((actual_width, height))
#screen2 = pygame.display.set_mode((width, height))
hidden_layer_size = 6

#these edges are lines that are going to be borders. best format but maybe laggy?



pygame.display.set_caption('this is my first go at it')


clock = pygame.time.Clock()


running = True

FPS = 10

col1 = (0,0,200)
time_limit = 5
current_time = 0
white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
weight_initial_range = 40
mutation_percent = 0.05
deg = math.pi / 2
car_x = 130
car_y = 200
car_width = 30
car_height = 15
degree_turn = math.pi / 60
#step_size is r
r = 0
Car_limit = 50
generation = 0
step_size = .56
LOOK_LIMIT = 100
friction = .3
magic_stop = .1
speed_limit = 9
edge = 50
#Line thickness makes collision easier, lazy fix
thickness = 10
line_detection_thickness = 3
halfthick = thickness / 2
line_edges = [((edge,edge),(width - edge,edge)),
              ((edge,edge),(edge,height - edge)),
              ((edge,height - edge),(width - edge,height - edge)),
              ((width - edge,edge),(width - edge,height - edge))]

obstacles = [((edge * 3, edge * 3),(edge * 3,(height -(edge * 3)))),
             ((edge * 5,  (height / 2)),(width - (edge * 2.5), (height / 2)))]

line_edges += obstacles



def convert_from_raw_coordinate(list_of_positions,axis_list):
    the_list = []
    y_change = 0
    x_change = 0

    for ((x1,y1),(x2,y2)),axis in zip(list_of_positions,axis_list):
        if axis == 0:
            x_change = halfthick
            y_change = 0
        else:
            x_change = 0
            y_change = halfthick


        first_cord = (x1 - x_change,y1 - y_change)
        second_cord = (x2 + x_change,y2 + y_change)
        the_list.append(first_cord + second_cord)
    return the_list

line_barrier_detection = convert_from_raw_coordinate(line_edges,[1,0,1,0,0,1])



#return-some form of placable rect
#no coordinates just size and color
def rect(h,w,c):
    r = pygame.Rect(0,0,h,w)


def rotate(img_surface, degree):
    rotsurf = pygame.transform.rotate(img_surface, math.degrees(-1 * degree))
    return rotsurf

#always specified at 0,0 as initial starting
def rectangle(width,height,col):
    surf = pygame.Surface((width,height),pygame.SRCALPHA)
    surf.fill(col)
    return surf

#this is bound locally by screen
def line(start_point,end_point, color,line_thickness = thickness):
    pygame.draw.line(screen, color, start_point, end_point,line_thickness)



def place_at(img, x, y):
    img_rectangle = img.get_rect()#this is not needed
    img_rectangle.center = (x,y)
    screen.blit(img,img_rectangle)

def draw_lines(list_of_lines):
    for point_one,point_two in list_of_lines:
        line(point_one,point_two, col1)

def draw_box(coord):
    thicky = 2
    colo = (255,0,255)
    line((coord[0],coord[1]),(coord[2],coord[1]),colo,thicky)
    line((coord[2],coord[1]),(coord[2],coord[3]),colo,thicky)
    line((coord[2], coord[3]), (coord[0], coord[3]), colo,thicky)
    line((coord[0], coord[3]), (coord[0], coord[1]), colo,thicky)

def draw_bbox(coord):

    thicky = 2
    colo = (255, 0, 255)
    line(coord[0], coord[2], colo, thicky)
    line(coord[2], coord[3], colo, thicky)
    line(coord[3], coord[1], colo, thicky)
    line(coord[1], coord[0], colo, thicky)

def create_text(text,size = 12,color = black):
    largeText = pygame.font.Font('freesansbold.ttf', size)
    textSurface = largeText.render(text, True, color)
    return textSurface

#box_hit_box = square_collision_detection(coordinates,barriars)
def square_collision_detection(box_coordinates,hit_box,radiu):
    #x = xcos - ysin
    #y = ycos + xsin
    car_width1 = car_width
    car_height1 = car_height
    fac = 2
    x1,y1 = box_coordinates[0],box_coordinates[1]
    new_theta = radiu + 0.523599
    new_theta2 = radiu - 0.523599
     #0 2 3 1

    vx1 = x1 - ((car_width / fac) * math.cos(new_theta))
    vy1 = y1 - ((car_width / fac) * math.sin(new_theta))
    xy1 = (vx1,vy1)#1

    vx2 = x1 + ((car_width / fac) * math.cos(new_theta))
    vy2 = y1 + ((car_width / fac) * math.sin(new_theta))
    xy2 = (vx2,vy2)#4

    vx3 = x1 - ((car_width / fac) * math.cos(new_theta2))
    vy3 = y1 - ((car_width / fac) * math.sin(new_theta2))
    xy3 = (vx3,vy3)#2

    vx4 = x1 + ((car_width / fac) * math.cos(new_theta2))
    vy4 = y1 + ((car_width / fac) * math.sin(new_theta2))
    xy4 = (vx4,vy4)#3

    lis = [xy1, xy3, xy4, xy2]
    #0,1
    #2,1
    #2,3
    #0,3

    by1 = (hit_box['y1'])
    by2 = (hit_box['y2'])
    bx1 = (hit_box['x1'])
    bx2 = (hit_box['x2'])
    full_package_line = np.r_['-1', bx1, by1, bx2, by2]

    hit_box = np.repeat(hit_box, len(lis))
    by1 = (hit_box['y1'])
    by2 = (hit_box['y2'])
    bx1 = (hit_box['x1'])
    bx2 = (hit_box['x2'])

    xs = np.array([vx1,vx2,vx3,vx4])#,dtype = [('x1',float),('x2',float),('x3',float),('x4',float)])
    xs = np.tile(xs,len(line_edges))

    ys = np.array([vy1, vy2, vy3, vy4])#,dtype = [('y1',float),('y2',float),('y3',float),('y4',float)])
    ys = np.tile(ys,len(line_edges))

    check_x = bx1 <= xs
    check_x2 = xs <= bx2

    check_y = by1 <= ys
    check_y2 = ys <= by2

    #here are the lines
    #vx1 vx3

    check_x3 = xs <= bx1
    check_x4 = bx1 <= xs

    check_y3 = ys <= by1
    check_y4 = by1 <= ys

    #print(lis)
    draw_bbox(lis)
    #full_package = np.r_['-1', xy1, xy2 , xy3, xy4]
    #full_package = full_package.reshape(4, bx1.shape[0])


    full_package_line = full_package_line.reshape(4, len(line_barrier_detection))
    #print(full_package)
    #df = np.vectorize(draw_box)
    #np.apply_along_axis(draw_bbox,0,full_package)
    #this one does the barriears(fullpackagelines)
    np.apply_along_axis(draw_box,0,full_package_line)

    #print(vx1[0],vy1[0],vx2[0],vy2[0])

    c1 = (check_x & check_x2) & (check_y & check_y2)
    c2 = (check_x3 & check_x4) & (check_y3 & check_y4)
    return c1 | c2

def within_square(point,square_size):
    check_x = square_size['x1'] <= point[0]
    check_x2 = point[0] <= square_size['x2']

    check_y = square_size['y1'] <= point[1]
    check_y2 = point[1] <= square_size['y2']
    return check_x & check_x2 & check_y & check_y2



def distance(x1,y1,x2,y2):
    xd = (x2 - x1) ** 2
    yd = (y2 - y2) ** 2
    return math.sqrt(xd + yd)



def find_distance_points(rotation,start_point_x,start_point_y):
    my_found_r, point_intersection = 0, (start_point_x, start_point_y)
    #can numpy go straight from an iterator?
    all_rad = list(range(0, LOOK_LIMIT * 10,int(step_size * 10)))
    all_rad = np.divide(all_rad,10) #array

    all_changes_y = np.multiply(all_rad, math.sin(rotation))
    all_changes_x = np.multiply(all_rad, math.cos(rotation))

    barrier_length = len(line_barrier_detection)
    total_number = len(line_barrier_detection) * all_rad.shape[0]

    the_car_x = np.add(all_changes_x,start_point_x)
    the_car_y = np.add(all_changes_y, start_point_y)
    the_car_x = np.tile(the_car_x,barrier_length)
    the_car_y = np.tile(the_car_y,barrier_length)#123,123
    barriars = np.array(line_barrier_detection, dtype = [('x1',float),('y1',float),('x2',float),('y2',float)])
    barriars = np.repeat(barriars, all_rad.shape[0])#111,222,333

    coordinates = (the_car_x,the_car_y)
    #I believe this does what i want up until now
    all_boolean_values = within_square(coordinates,barriars)

    full_package = np.r_['-1',all_boolean_values,np.tile(all_rad,barrier_length)
    ,the_car_x,the_car_y]

    full_package = full_package.reshape(4,total_number)
    #weeded_out = full_package[full_package == np.array([1,any,_,_])]
    index = np.where(all_boolean_values == True)[0]

    complete_radiuses = np.tile(all_rad,barrier_length)


    if (index.shape[0] > 0) :
        #
        #my_found_r = all_rad[index_r]
        the_radiuses = complete_radiuses[index]
        #my_found_r = np.argpartition(the_radiuses, 0)[0]
        my_found_r = np.amin(the_radiuses)

        end_point_y = (my_found_r * math.sin(rotation)) + start_point_y
        end_point_x = (my_found_r * math.cos(rotation)) + start_point_x
        point_intersection = (end_point_x,end_point_y)

        #point_intersection = (the_car_x[index_r][0],the_car_y[index_r][0])











    return my_found_r, point_intersection




def sigmoid(x):
    value = 1 / (1 + math.e ** -x)
    return value

class Brain:
    """this is a brain"""
    def __init__(self,input_size,hidden_size,output_size):
        func = np.vectorize(lambda x : random.randint(-weight_initial_range, weight_initial_range))


        self.input_column = np.zeros([input_size,1],dtype = float)
        self.hidden_column = np.zeros([hidden_size,1], dtype = float)#kinda useless
        self.output_column = np.zeros([output_size,1],dtype = float)#kinda useless

        self.input_hidden_weight = func(np.zeros([hidden_size,input_size],dtype = float))
        self.hidden_output_weight = func(np.zeros([output_size,hidden_size],dtype = float))

    def set_input(self,the_input):
        #the_input is a list
        self.input_column = np.transpose(np.array(the_input))

    def think(self):
        #feedforward proccess
        func = np.vectorize(sigmoid)

        self.hidden_column = func(self.input_hidden_weight @ self.input_column)
        self.output_column = func(self.hidden_output_weight @ self.hidden_column)

        return self.output_column



        #these sizes should just be how many nodes are in each layer
        #so 3 layer total

class Car:
    """This Is A Car"""


    def __init__(self):
        #r is currently not being changed
        self.car_x = car_x
        self.car_y = car_y
        self.deg = deg
        self.currentdistances = [0,0,0]
        #"STRAIGHT" "LEFT" "RIGHT"
        self.movement = "STRAIGHT" #redundant??
        self.r = 7


        self.my_brain = Brain(3, hidden_layer_size, 2)
        #should it start thinking right away?
        #self.my_brain.set_input(self.currentdistances)
        self. alive = True
        self.fitness = 0

    def get_fitness(self):
        return self.fitness

    def Increment_Fitness(self):
        if self.alive :
            self.fitness += 1/FPS
            self.fitness += self.r / (speed_limit + 10)

    def affect_velocity(self):
        self.prediction = self.my_brain.think()
        speed_up = self.prediction[0] > .5
        if not(self.alive):
            self.r = 0

        if speed_up:
            self.r = self.r + step_size

        if self.r > 0:
            self.r = self.r - friction
            # this caps the speed. There gotta be some kind of range for this though
        if self.r >= speed_limit:
            self.r = speed_limit
        elif self.r <= magic_stop:
            self.r = 0
            self.alive = False
            #didn't want to make stopping deathly in all cases
            #but i did here to debug it





        #self.dx = 0
        #self.dy = 0

    def adjustMovement(self):
        self.my_brain.set_input([x / width for x in self.currentdistances])
        self.prediction = self.my_brain.think()

        self.prediction = self.prediction[1]
        can_move = self.r > 0 and self.alive

        #change this if statement to some a little neater
        if 0.0 <= self.prediction < .4 and can_move:
            self.movement = "LEFT"
            self.deg -= degree_turn
        elif .4 <= self.prediction <= .6 and can_move:
            self.movement = "STRAIGHT"

        elif .6 < self.prediction <= 1.0 and can_move:
            self.movement = "RIGHT"
            self.deg += degree_turn


    def detectCollision(self):
        barrier_length = len(line_barrier_detection)
        the_car_x = self.car_x
        the_car_y = self.car_y
        #the_car_x = np.tile(the_car_x, barrier_length)
        #the_car_y = np.tile(the_car_y, barrier_length)  # 123,123

        barriars = np.array(line_barrier_detection, dtype=[('x1', float), ('y1', float), ('x2', float), ('y2', float)])
        coordinates = (the_car_x, the_car_y)
        box_hit_box = square_collision_detection(coordinates,barriars,self.deg)
        #box_hit_box = within_square(coordinates,barriars)

        index = np.where(box_hit_box == True)[0]
        #(index.shape[0] > 0):
        if np.any(box_hit_box):
            self.alive = False

    def mutate(self):
        for x in range(0, len(self.my_brain.input_hidden_weight)):
            if (random.randint(0, 101) / 100) <= mutation_percent:
                self.my_brain.input_hidden_weight[x] = random.randint(-weight_initial_range, weight_initial_range)

        for x in range(0,len(self.my_brain.hidden_output_weight)):
            if (random.randint(0, 101) / 100) <= mutation_percent:
                print("I am mutating")
                self.my_brain.hidden_output_weight[x] = random.randint(-weight_initial_range, weight_initial_range)



    def combine(self, a_car):
        new_car = Car()

        my_hidden_weights = self.my_brain.input_hidden_weight
        my_output_weights = self.my_brain.hidden_output_weight

        car_hidden_weights = a_car.my_brain.input_hidden_weight
        car_output_weights = a_car.my_brain.hidden_output_weight

        #not a bad option but I don't like it
        #new_car.my_brain.input_hidden_weights = (my_hidden_weights + car_hidden_weights) / 2
        #new_car.my_brain.hidden_output_weight = (my_output_weights + car_output_weights) / 2
        for x in range(0, len(my_hidden_weights)):
            if (random.randint(0, 101) / 100) > .5:
                new_car.my_brain.input_hidden_weight[x] = my_hidden_weights[x]
            else:
                new_car.my_brain.input_hidden_weight[x] = car_hidden_weights[x]

        for x in range(0, len(my_output_weights)):
            if (random.randint(0, 101) / 100) > .5:
                new_car.my_brain.hidden_output_weight[x] = my_output_weights[x]
            else:
                new_car.my_brain.hidden_output_weight[x] = car_output_weights[x]

        return new_car


    def move(self):
        #updates the coordinates
        if self.alive :
            self.dy = self.r * math.sin(self.deg)
            self.dx = self.r * math.cos(self.deg)
            self.car_x = self.car_x + self.dx
            self.car_y = self.car_y + self.dy





    def draw(self):

        #draws a square on the screen
        self.my_image = rectangle(car_width, car_height, col1)
        self.my_image = rotate(self.my_image, self.deg)
        place_at(self.my_image, self.car_x, self.car_y)

    def drawLines(self):
        # drawing the distance lines

        ref_degree = self.deg
        self.currentdistances = []
        for new_degree in [ref_degree,ref_degree - (math.pi / 4), ref_degree + (math.pi / 4)]:
            found_r, the_cord_found = find_distance_points(new_degree, self.car_x, self.car_y)
            self.currentdistances.append(found_r)
            line((self.car_x, self.car_y), the_cord_found, (255, 0, 0), line_detection_thickness)


class Widget:
    def __init__(self):
        # (self,x,y,width,height)function?
        self.button_function = lambda : print("This button Does Nothing")
        self.label = "An Empty Widget"
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.color = (0, 0, 255, 255)

    def update(self):
        pass

    #dont think this will have many uses
    def set_function(self,new_function):
        self.button_function = new_function

    #gotta make this inhertied somehow from panel
    def set_params(self,x,y,button_width,button_height):
        self.x = x
        self.y = y
        self.width = button_width
        self.height = button_height



    def button_down(self):
        #self.color = (0, 0, 255, 0)
        self.button_function()


    def button_up(self):
        #self.color = (0, 0, 255, 255)
        pass

    def draw_self(self):
        box = rectangle(self.width,self.height,self.color)
        place_at(box,self.x,self.y)


# draw_self() | button_up() | button_down() | set_params(x,y,w,h)
# set_function(function)


class Button(Widget):
    """This Is A Button"""
    def __init__(self):
        Widget.__init__(self)
        self.label = "Button"
        self.target = 0

class Preview(Widget):
    """This Is Supposed To display Numbers/Strings"""
    def __init__(self):
        Widget.__init__(self)
        self.label = "Window_Box"
        self.color = (100,100,100,100)
        self.target = 0
        self.button_function = 0

    #just vetoing all the useless functions?
    def button_up(self):
        pass
    def button_down(self):
        pass
    def set_function(self,new_function):
        pass

    def update(self):
        pass

    #update function?
    def set_monitor(self,obj):
        self.target = [obj]


    def draw_self(self):
        Widget.draw_self(self)
        words = create_text(str(self.target[0]),int(self.height / 2))
        place_at(words, self.x,self.y)



class Slider(Widget):
    """This Is A Slider"""
    def __init__(self):
        Widget.__init__(self)
        self.label = "Slider"
        self.value = 0
        self.start = 30
        self.end = 100
        self.color = (100,100,100,100)
        self.slider_value = self.value

    def set_function(self,new_function):
        self.button_function = new_function

    def limits(self,start,end):
        self.start = start
        self.end = end

    def get_value(self):
        return self.value
    def set_value(self,value):
        self.value = value

    def set_params(self,x,y,button_width,button_height):
        Widget.set_params(self,x,y,button_width,button_height)
        self.height = (1/3) * self.height

    def button_down(self):

        (x, y) = pygame.mouse.get_pos()
        x1 = self.x - self.width
        raw_x = x - x1
        #self.value = (raw_x / (self.x + (self.width / 1))) * self.end

        # so we can show it correctly(display wise)
        self.slider_value = np.interp(x, [self.x - (self.width / 2), self.x + (self.width / 2)], [0, self.width])
        self.value = np.interp(self.slider_value, [0, self.width], [self.start, self.end])
        self.button_function()


    def draw_self(self):
        #This function looks soooo ugly
        #gotta be another way
        # circle(Surface, color, pos, radius, width=0)
        #pygame.draw.circle(screen, blue, (150, 150), 5, 1)


        Widget.draw_self(self)
        calc_x = self.x - (self.width / 2) + self.slider_value

        pygame.draw.circle(screen,black,(int(calc_x),int(self.y)),int(self.height),1)



class Panel:
    def __init__(self,width_size,height_size):
        self.width = width_size
        self.height = height_size
        self.widget_list = []
        self.x = 0
        self.y = 0
        self.vertical_padding = 10
        self.horizontal_padding = 0
        self.widget_height = 20
        self.widget_width = self.width - (2 * self.horizontal_padding)

    def add(self,widget):
        #x_pad,y_pad,x,y,width,height)
        base_y = self.y - self.height + (self.widget_height / 2)
        base_y = base_y + (len(self.widget_list) * (self.widget_height + self.vertical_padding))
        #base_y = base_y + len(self.widget_list) * self.vertical_padding
        #base_y = base_y + (len(self.widget_list) / 2) * len(self.widget_list) + 1

        widget.set_params(self.x,base_y,self.widget_width,self.widget_height)

        self.widget_list.append(widget)

    def set_panel_location(self,x_coordinate,y_coordinate):
        self.x = x_coordinate
        self.y = y_coordinate

    def draw_buttons(self):
        func = lambda x : x.draw_self()
        fvect = np.vectorize(func)
        fvect(self.widget_list)


    #line(start_point,end_point, color,line_thickness = thickness)
    #debug stuff, should be deprecated later
    def draw_panel_outline(self):
        x1,y1 = self.x - self.width,self.y - self.height
        x2, y2 = self.x + self.width, self.y + self.height
        line((x1,y1),(x1,y2),black,1)
        line((x2, y1), (x2, y2), black,1)

    def update(self): #DELETE
        f = np.vectorize(lambda x : x.update())
        f(self.widget_list)

    def event_handler(self,event):
        x1, y1 = self.x - self.width, self.y - self.height
        x2, y2 = self.x + self.width, self.y + self.height
        (x,y) = pygame.mouse.get_pos()
        button_index = (y - y1) // (self.widget_height + self.vertical_padding)

        #now we check for click on buttong and not just white space
        real_y = max(button_index , 0) * (self.widget_height + self.vertical_padding)
        on_button = real_y < (y - y1) < (real_y + self.widget_height)
        on_button = on_button and button_index < len(self.widget_list)
        #pad_x = x1 + self.horizontal_padding < x < x2 - self.horizontal_padding


        if pygame.mouse.get_pressed() == (1,0,0) and x1 < x < x2 and y1 < y <y2 and on_button:
            self.widget_list[int(button_index)].button_down()
            self.widget_list[int(button_index)].button_up()
            #here to debug stuff
            #print("mouse was pressed + {}".format(button_index))



car_population = [Car() for x in range(0,Car_limit)]
numpy_population = np.array(car_population)
winner_number = 4

def make_from_potluck(fittest):
    new_population = []
    potluck = []
    for x,y in zip(fittest, [x ** 3 for x in range(len(fittest),0,-1)]):
        replicated_car = [x] * y
        potluck.extend(replicated_car)

    #print(len(potluck))
    while len(new_population) < Car_limit:
        #print(len(new_population))
        indx1 = random.randint(0,len(potluck) - 1)
        indx2 = random.randint(0,len(potluck) - 1)
        new_car = potluck[indx1].combine(potluck[indx2])
        new_car.mutate()
        new_population.append(new_car)
    new_population + [Car() for x in range(0,10)]
    return new_population


def grab_highest(a_population):
    winners = np.array([])

    get_fitness = np.vectorize(lambda x: x.get_fitness())
    fitness_values = get_fitness(a_population)

    while len(winners) < winner_number:
        maximum = np.amax(fitness_values)
        index = fitness_values == maximum
        the_win = a_population[index]
        winners = np.append(winners,the_win[0:winner_number - len(winners)])

    # print(winners)
    return winners



#DO NOT INITIALIZE INSIDE OF LOOP
#YOUR GONNA REGRET IT

#These variables are for genetic algorithm
#These variables are for the buttons and whatnot

panel_offset = 80
label_panel = Panel(50,100 + panel_offset)
label_panel.set_panel_location(width + ((actual_width - width)/ 4),150 + panel_offset)
label_panel.widget_width = label_panel.widget_width * 1.5

preview_panel = Panel(50,100 + panel_offset)
preview_panel.set_panel_location(width + ((actual_width - width) * 2/ 4),150 + panel_offset)

slider_panel = Panel(50,100 + panel_offset)
slider_panel.set_panel_location(width + ((actual_width - width) * 3/ 4),150 + panel_offset)


list_of_panels = [preview_panel,slider_panel,label_panel]

panel_draw = np.vectorize(lambda x : x.draw_panel_outline())
button_draw = np.vectorize(lambda x : x.draw_buttons())
panel_event = np.vectorize(lambda x : x.event_handler(event))

#generation monitor
gen = Slider()
gen_label = Preview()
gen_label.set_monitor("GENERATION")
gen_count = Preview()

#frames monitor
fps_bar = Slider()
fps_count = Preview()
fps_label = Preview()
fps_label.set_monitor("FPS")
fps_bar.limits(1,60)
def set_fps():
    global FPS
    FPS = int(fps_bar.get_value())

fps_bar.set_function(set_fps)

#generic
"""fps_bar = Slider()
fps_count = Preview()
fps_label = Preview()
"""
#generic

#evolution time monitor
time_limit_bar = Slider()
time_limit_bar.limits(1,50)
time_limit_count = Preview()
time_limit_label = Preview()
time_limit_label.set_monitor("Time Limit")
time_limit_count.set_monitor(time_limit)
def set_time_limit():
    global time_limit
    time_limit = int(time_limit_bar.get_value())
time_limit_bar.set_function(set_time_limit)

#how many in generation monitor
generation_bar = Slider()
generation_count = Preview()
generation_label = Preview()
generation_label.set_monitor("GenSize(current)")
generation_count.set_monitor(len(car_population))

#mutation monitor
mutation_bar = Slider()
mutation_bar.limits(0,1)
mutation_count = Preview()
mutation_label = Preview()
mutation_label.set_monitor("MutationRate")
mutation_count.set_monitor(mutation_percent)
def set_mutation_percent():
    global mutation_percent
    mutation_percent = mutation_bar.get_value()

mutation_bar.set_function(set_mutation_percent)
#this is pretty ugly but it works

#current_time
current_time_bar = Slider()
current_time_count = Preview()
current_time_label = Preview()
current_time_label.set_monitor("TIME IS:")
current_time_count.set_monitor(current_time)

#changing population size
pop_size_bar = Slider()
pop_size_bar.limits(1,100)
pop_size_count = Preview()
pop_size_label = Preview()
pop_size_label.set_monitor("Car Pop:")
pop_size_count.set_monitor(Car_limit)
def set_car_pop():
    global Car_limit
    Car_limit = int(pop_size_bar.get_value())

pop_size_bar.set_function(set_car_pop)

#adjusting brain parameter(weights)
param_bar = Slider()
param_bar.limits(10,100)
param_count = Preview()
param_label = Preview()
param_label.set_monitor("WeightInitRange")
param_count.set_monitor(weight_initial_range)
def set_param_init():
    global weight_initial_range
    weight_initial_range = int(param_bar.get_value())

param_bar.set_function(set_param_init)

#The degree in which everything spawn in
deg_bar = Slider()
deg_bar.limits(0,2 * math.pi)
deg_count = Preview()
deg_label = Preview()
deg_label.set_monitor("DegreeSpawn")
deg_count.set_monitor(deg)
def set_deg():
    global deg
    deg = deg_bar.get_value()
deg_bar.set_function(set_deg)

#hidden layer size for brain
layer_bar = Slider()
layer_bar.limits(3,10)
layer_count = Preview()
layer_label = Preview()
layer_label.set_monitor("BrainSize|restartsSim")
layer_count.set_monitor(hidden_layer_size)
def set_layer_size():
    global hidden_layer_size,car_population
    hidden_layer_size = int(layer_bar.get_value())
    car_population = [Car() for x in range(0, Car_limit)]

layer_bar.set_function(set_layer_size)

#how far can the cars see
sight_bar = Slider()
sight_bar.limits(10,width)
sight_count = Preview()
sight_label = Preview()
sight_label.set_monitor("SightDistance")
sight_count.set_monitor(LOOK_LIMIT)
def set_look_limit():
    global LOOK_LIMIT
    LOOK_LIMIT = int(sight_bar.get_value())
sight_bar.set_function(set_look_limit)

#speed_limit
speed_limit_bar = Slider()
speed_limit_bar.limits(2,13)
speed_limit_count = Preview()
speed_limit_label = Preview()
speed_limit_label.set_monitor("SpeedLimit")
speed_limit_count.set_monitor(speed_limit)
def set_speed_limit():
    global speed_limit
    speed_limit = int(speed_limit_bar.get_value())
speed_limit_bar.set_function(set_speed_limit)





#for sliding values
slider_panel.add(gen)
slider_panel.add(fps_bar)
slider_panel.add(time_limit_bar)
slider_panel.add(generation_bar)
slider_panel.add(mutation_bar)
slider_panel.add(current_time_bar)
slider_panel.add(param_bar)
slider_panel.add(pop_size_bar)
slider_panel.add(deg_bar)
slider_panel.add(layer_bar)
slider_panel.add(sight_bar)
slider_panel.add(speed_limit_bar)

#for number values
preview_panel.add(gen_count)
preview_panel.add(fps_count)
preview_panel.add(time_limit_count)
preview_panel.add(generation_count)
preview_panel.add(mutation_count)
preview_panel.add(current_time_count)
preview_panel.add(param_count)
preview_panel.add(pop_size_count)
preview_panel.add(deg_count)
preview_panel.add(layer_count)
preview_panel.add(sight_count)
preview_panel.add(speed_limit_count)

#labels everything
label_panel.add(gen_label)
label_panel.add(fps_label)
label_panel.add(time_limit_label)
label_panel.add(generation_label)
label_panel.add(mutation_label)
label_panel.add(current_time_label)
label_panel.add(param_label)
label_panel.add(pop_size_label)
label_panel.add(deg_label)
label_panel.add(layer_label)
label_panel.add(sight_label)
label_panel.add(speed_limit_label)

while running:
    screen.fill(white)


    #point the variables here
    gen_count.set_monitor(generation)
    fps_count.set_monitor(FPS)
    time_limit_count.set_monitor(time_limit)
    generation_count.set_monitor(len(car_population))
    mutation_count.set_monitor(mutation_percent)
    current_time_count.set_monitor(str(current_time)[:4])
    param_count.set_monitor(weight_initial_range)
    pop_size_count.set_monitor(Car_limit)
    deg_count.set_monitor(str(deg * 180 / math.pi)[:4])
    layer_count.set_monitor(hidden_layer_size)
    sight_count.set_monitor(LOOK_LIMIT)
    speed_limit_count.set_monitor(speed_limit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        panel_event(list_of_panels)

    panel_draw(list_of_panels)
    button_draw(list_of_panels)
    current_time += 1/FPS

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        #best_cars = grab_highest(car_population)
        car_population = [Car() for x in range(0, Car_limit)]
        generation = 0
        FPS = 15
        time_limit = 5
        current_time = 0
        Car_limit = 50
        mutation_percent = .05
        weight_initial_range = 40




    v_get_fitness = np.vectorize(lambda x : x.get_fitness())
    v_get_alive = np.vectorize(lambda x: not x.alive )
    death_clock = current_time > time_limit

    #GENETIC ALGO STARTS HERE
    if death_clock or np.all(v_get_alive(numpy_population)):
        #car_population = [Car() for x in range(0, Car_limit)]
        highest_population = grab_highest(numpy_population)
        car_population = make_from_potluck(highest_population)
        current_time = 0
        generation += 1


    draw_lines(line_edges)



    #can i vectorize this????
    #vectorize(affectvelocity) or sum of the like.
    dc = np.vectorize(lambda x : x.detectCollision())
    av = np.vectorize(lambda x: x.affect_velocity())
    am = np.vectorize(lambda x: x.adjustMovement())
    m = np.vectorize(lambda x: x.move())
    dl = np.vectorize(lambda x: x.drawLines())
    inf = np.vectorize(lambda x: x.Increment_Fitness())
    dr = np.vectorize(lambda x: x.draw())
    al = np.vectorize(lambda x: x.alive)

    numpy_population = np.array(car_population)

    I = al(numpy_population)
    vehicle = numpy_population[I]
    #need to use better names
    dc(vehicle)
    av(vehicle)
    am(vehicle)
    m(vehicle)
    dl(vehicle)
    inf(vehicle)
    dr(numpy_population)


    #3  * math.pi / 2

    """"#ind_distance_2(p1,t1,r1,p2,t2):
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:

        deg = deg - degree_turn

    elif keys[pygame.K_RIGHT]:

        deg = deg + degree_turn

    """
    #I believe this line seperates the 2 borders
    line((width, 0), (width, height), (0, 0, 0), 4)
    pygame.display.update()
    clock.tick(FPS)




pygame.quit()
quit()