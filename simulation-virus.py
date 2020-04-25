import pygame
from random import randint, choice
import time
    
 
def circle_inside(x_y,food):
  if x_y[0] >= food[0] and x_y[0] <= food[0] + 20:
    if x_y[1] >= food[1] and x_y[1] <= food[1] + 20:
      return True
pygame.init()
win = pygame.display.set_mode((900, 500))
pygame.display.set_caption('Симуляция COVID19')
done = False
pedometer = 0
x_change = 0
y_change = 0
breaks = True
mans = []
quantity_sick = 50
for i in range(quantity_sick):
  random_coordinates_x = randint(1, 480)
  random_coordinates_y = randint(1, 480)
  man = pygame.Rect(random_coordinates_x, random_coordinates_y, 6, 6)
  mans.append(man)
 
base_color = {}
colors = []
for i in range(quantity_sick):
  colors.append('color' + str(i + 1))
  base_color[colors[i]] = (255,255,255)

def side_of_movement(moves):
  array = [0,1,2,3]
  array.remove(moves)
  return choice(array)
 
def traffic(position_robot, moves):
  global x_change
  global y_change
  global pedometer
 
  x = position_robot[0]
  y = position_robot[1]
  pedometer += 1
  #right
  if moves == 0:
    x_change = 2
    y_change = 0
    x += x_change
    y += y_change
    side_x = x + 3
    side_y = y
  #left
  if moves == 1:
    x_change = -2
    y_change = 0
    x += x_change
    y += y_change
    side_x = x
    side_y = y
  #down
  if moves == 2:
    y_change = 2
    x_change = 0
    x += x_change
    y += y_change
    side_x = x
    side_y = y + 3
  #up
  if moves == 3:
    y_change = -2
    x_change = 0
    x += x_change
    y += y_change
    side_x = x
    side_y = y
 
  return [side_x, side_y, pedometer, x, y]
 
sick_people = {}
for i in range(len(colors)):
  sick_people[colors[i]] = "healthy"
 
sick_people[colors[5]] = "sick"
 
def position_man(man, moves):
  global pedometer
  color_man = moves[1]
  moves = moves[0]
  if pedometer % 15 == 0:
    moves = side_of_movement(moves)
 
  result = traffic((man.x, man.y), moves)
  side_x = result[0]
  side_y = result[1]
  pedometer = result[2]
  man.x = result[3]
  man.y = result[4]
  if side_x >= 500 or side_x <= 0 or side_y >= 500 or side_y <= 0:
    position = side_y + side_x
    moves = side_of_movement(moves)
    if side_x >= 500:
      man.x -= 6
    if side_x <= 0:
      man.x += 6
    if side_y >= 500:
      man.y -= 6
    if side_y <= 0:
      man.y += 6
 
  global sick_people
  global mans
  global colors
  mans_proba = []
  colors_proba = []
  for i in range(len(mans)):
    mans_proba.append(mans[i])
    colors_proba.append(colors[i])

  mans_proba.remove(man)
  colors_proba.remove(color_man)
  state = "healthy"
  radius = 0
  color = 0
  if sick_people[color_man] == "sick":
    radius = pygame.Rect(man.x-7, man.y-7, 20, 20)
    for i in range(len(mans_proba)):
      if radius.colliderect(mans_proba[i]):
        state = "sick"
        color = colors_proba[i]
        break
 
  return [man, moves, state, radius, color]

movess = []
for i in range(quantity_sick):
  moves = randint(0,3)
  movess.append(moves)

#больной
sicks = 0
array_sicks = []
now = time.time()
future = now + 1
times = 0

graphik = []

while not done:
  pygame.time.delay(100)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True

  win.fill((255, 255, 255))
  pedometer += 1
  u = 10
  x2 = 530
  text_time = pygame.font.Font(None, 15)
  text_time = text_time.render('Время в с.', True, (0, 0, 0))
  win.blit(text_time, (840, 465))
  text_time = pygame.font.Font(None, 15)
  text_time = text_time.render('Количество больных', True, (0, 0, 0))
  win.blit(text_time, (525, 30))

  for d in range(18):
    time_x = pygame.font.Font(None, 14)
    u = str(u)
    text_time_x = time_x.render(u, True, (0, 0, 0))
    win.blit(text_time_x, (x2, 450))
    pygame.draw.line(win, (0,0,0), (x2,442),(x2, 438), 2)
    x2 += 20
    u = int(u)
    u += 10

  z = 0
  y2 = 430
  for d in range(5):
    time_x = pygame.font.Font(None, 14)
    z = str(z)
    text_time_x = time_x.render(z, True, (0, 0, 0))
    win.blit(text_time_x, (505, y2))
    pygame.draw.line(win, (0,0,0), (518,y2),(522,y2), 2)
    y2 -= 100
    z = float(z)
    z += 0.5

  for i in range(quantity_sick):
    if time.time() > future:
      now = time.time()
      future = now + 1
      times += 1

  for i in range(len(graphik)):
    pygame.draw.line(win, (160,6,9), (graphik[i][0]), (graphik[i][1]), 2)
    if i > 1:
      d = i - 1
      x_line = graphik[d][1][0] - 1
      y_line = graphik[d][1][1]
      pygame.draw.line(win, (160,6,9), (x_line, y_line), (graphik[i][0]), 2)

  pygame.display.update()
  
  for i in range(quantity_sick):   
    result_position = position_man(mans[i], (movess[i], colors[i]))
    movess[i] = result_position[1]
    position = result_position[0]

    #цвет заразившигося
    if result_position[2] == "sick":
      sick_people[result_position[4]] = "sick"
 
    if sick_people[colors[i]] == "sick":
      if colors[i] not in array_sicks:
        array_sicks.append(colors[i])
        sicks += 1
 
      if colors[i] in array_sicks:
        template_test_sicks = pygame.font.Font(None, 18)
        text_sicks = template_test_sicks.render('Заболевших: ' + str(sicks), 1, (180, 0, 0))
        win.blit(text_sicks, (520, 10))
        pygame.draw.rect(win, (246,155,156), result_position[3])
        pygame.display.update()
    pygame.draw.rect(win, (0,0,0), position)
    pygame.draw.line(win, (160,6,9), (502,0),(502, 500), 2)
    pygame.draw.line(win, (0,0,0), (520,30), (520, 440), 2)
    pygame.draw.line(win, (0,0,0), (520,440), (880, 440), 2)
    pygame.display.update()

  percentage = (sicks * 100) / quantity_sick
  y_graphik = 430 - (400 * percentage) / 100
  graphik.append([[times + 530, y_graphik], [times + 530 + 2, y_graphik]])

pygame.quit()
