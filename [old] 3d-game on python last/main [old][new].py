# Импорт pygame и остальных библиотек
import pygame
from os import path
import math

# Константы
WxH = [800, 600]
FPS = 30 # Частота обновления экрана
running = True # Цикл работы окна
FOV = 60 # Угол обзора в градусах

# Импорт изображений
img_dir = path.join(path.dirname(__file__), 'img')

# Инициализация pygame
pygame.init()
# Создание окна
screen = pygame.display.set_mode(WxH)
pygame.display.set_caption("Unperspective")
clock = pygame.time.Clock()
#font_name = pygame.font.match_font('arial')

# Функции
# Нахлждение растояния до стены (новая)
def wallcross(p1, ang, p3, p4):    
    # Нахождение промежуточной точки
    p2 = [(p1[0] + 50 * math.sin(math.radians(ang))),
          (p1[1] - 50 * math.cos(math.radians(ang)))]
    #pygame.draw.circle(screen, (0, 255, 0), p2, 5)
    
    # Нахождение промежуточной переменной
    n = (p1[0] - p2[0])*(p3[1] - p4[1]) - (p1[1] - p2[1])*(p3[0] - p4[0])
    if n != 0:
        # Нахождение точек
        cx = ((p1[0]*p2[1] - p1[1]*p2[0]) * (p3[0]-p4[0]) -
              (p1[0]-p2[0]) * (p3[0]*p4[1] - p3[1]*p4[0]))/n
        
        cy = ((p1[0]*p2[1] - p1[1]*p2[0]) * (p3[1]-p4[1]) -
              (p1[1]-p2[1]) * (p3[0]*p4[1] - p3[1]*p4[0]))/n

        # Нахождение расстояния от p1 до точки пересечения
        dst = math.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
        # Проверка нахождения точки в диапазоне
        if ((cx >= min(p3[0], p4[0])-0.05) and
            (cx <= max(p3[0], p4[0])+0.05) and
            (cy >= min(p3[1], p4[1])-0.05) and
            (cy <= max(p3[1], p4[1])+0.05)
            and ((p1[0]-p2[0]) * (p1[0] - cx) > 0)):
            pygame.draw.circle(screen, (255, 0, 0), (cx, cy), 4)
            #pygame.draw.line(screen, (0, 255, 255), (cx, cy), p1)

            # Нахождение растояния до p3
            wld = (math.sqrt((cx - p3[0])**2 + (cy - p3[1])**2))

            # Проверка возможности такой стены
            if dst != 0:
                k = min((5*WxH[1] / dst), WxH[1])
                return [k, wld] 

            else:
                return [WxH[1], wld]
        else:         
            #pygame.draw.circle(screen, (255, 255, 0), (cx, cy), 5)
            return 0
    else:
        return 0


# Отрисовка стены
def walldraw(h, cycle, dH, dl):
    # Новая отрисовка
    #img = wallimg.fill((0, 0, min(2*h, 255), 100), special_flags = pygame.BLEND_MULT) # Изменение цвета столбца
    wall_column = wallimg.subsurface((dl % 10)*120, 0, 1, 1200)
    wall_columnn = pygame.transform.scale(wall_column, (1, 2*h))
    screen.blit(wall_columnn, (cycle, WxH[1]//2-h))

# Функция чтения файла стен
def wallread(filename):
    # Чтение файла
    file = open(filename, "r")
    st = file.read().split("Walls:")
    # Закрытие файла массива стен
    file.close()

    # Создание массива точек стен
    global points
    points = []
    for i in st[0].split("\n"):
        if i and i != "Points:":
            pnt = i.split(", ")
            points.append( [int(pnt[0]), int(pnt[1])] )

    # Создание массива стен через точки
    global walls
    walls = []
    for i in st[1].split("\n"):
        if i:
            pnt = i.split(", ")
            walls.append( [int(pnt[0]), int(pnt[1])] )


# Класс игрока
class Player():
    def __init__(self, X, Y, angle):
        self.x = X
        self.y = Y
        self.rot = angle
        self.speedx = 0
        self.speedy = 0

    def update(self):
        # Проверка нажатия клавиш
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.speedx = 2
        if keystate[pygame.K_s]:
            self.speedx = -2

        if keystate[pygame.K_d]:
            self.speedy = -2
        if keystate[pygame.K_a]:
            self.speedy = 2

        # Бег на shift
        if keystate[pygame.K_LSHIFT]:
            self.speedx *= 2
            self.speedy *= 2

        # Поворот на стрелочки
        if keystate[pygame.K_LEFT]:
            self.rot -= 5
        if keystate[pygame.K_RIGHT]:
            self.rot += 5

        # Переключение карт
        if keystate[pygame.K_1]:
            wallread("walls1.txt")
        if keystate[pygame.K_2]:
            wallread("walls2.txt")

        # Изменение угла благодаря курсору
        self.rot = int(self.rot + (-WxH[0]//2 + pygame.mouse.get_pos()[0])/2) % 360

        # Возврат курсора в изночальное положение
        pygame.mouse.set_pos((WxH[0]//2, WxH[1]//2))

        sinx = math.sin(math.radians(self.rot))
        cosx = math.cos(math.radians(self.rot))

        # Изменение координаты в зависимости от угла и нажатия клавиш
        self.x += self.speedx * sinx
        self.x -= self.speedy * cosx

        self.y -= self.speedx * cosx
        self.y -= self.speedy * sinx

        self.speedx = 0
        self.speedy = 0

# Загрузка графики
# Загрузка изображения стены
wallimg = pygame.image.load(path.join(img_dir, "1.png")).convert()
# Загрузка изображения пола
floorimg = pygame.image.load(path.join(img_dir, "2.png")).convert()

# Загрузка списка стен из файла
wallread("walls1.txt")

# Список объектов для обновления
objects = []

# Создание объектов в мире
# Создание игрока
ply = Player(140, 160, 270);
objects.append(ply) # Добавление игрока к списку обновляемых объектов

# Убираем курсор
pygame.mouse.set_visible(False)

# Запуск самой программы
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)

    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
    
    # Обновление всех объектов
    for i in objects:
        i.update()

    # Рендеринг
    # Запоняем экран цветом неба
    screen.fill((0, 255, 255))

    # Отрисовка иллюзии пола
    pygame.draw.rect(screen, (127, 127, 127), ((0, WxH[1]//2), (WxH[0], WxH[1])))

    # Отрисовка псевдо-трёхмерных стен
    for i in range(WxH[0]):
        # Нахождение пересечения со стеной
        dst = [] # Список расстояний до стен
        ld = [] # Растояние от стен
        ang = i*FOV/WxH[0] - FOV//2 + ply.rot # Угол просчёта
        #print(ang, i, ply.rot, i*FOV/WxH[0])

        # Нахождение пересечений со стенами
        for j in walls:
            c = wallcross((ply.x, ply.y), ang, points[j[0]], points[j[1]] )
            if c != 0:
                dst.append(c[0])
                ld.append(c[1])
                
        # Отрисовка стены
        if (dst != []) and (min(dst) != 0):
            walldraw( max(dst), i, 0, ld[ dst.index(max(dst)) ] )

    # Отрисовка миникарты для отладки
    for i in walls:
        # Отрисовка стен
        pygame.draw.line(screen, (127, 127, 127), points[i[0]], points[i[1]])

    # Отрисовка игрока
    pygame.draw.circle(screen, (0, 0, 0), (ply.x, ply.y), 5)
    # Отрисовка поля зрения
    pygame.draw.line(screen, (128, 128, 128), (ply.x, ply.y),
                     ((ply.x + 30*math.sin(math.radians(ply.rot-FOV//2))),
                      (ply.y - 30*math.cos(math.radians(ply.rot-FOV//2)))))
    pygame.draw.line(screen, (128, 128, 128), (ply.x, ply.y),
                     ((ply.x+30*math.sin(math.radians(ply.rot+FOV//2))),
                      (ply.y-30*math.cos(math.radians(ply.rot+FOV//2)))))

    # А это что за лининия?
    # А, это линия центра зрения
    """pygame.draw.line(screen, (128, 128, 128), (ply.x, ply.y),
                     ((ply.x+20*math.sin(math.radians(ply.rot))),
                      (ply.y-20*math.cos(math.radians(ply.rot)))))"""
    
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

# Включение курсора
pygame.mouse.set_visible(True)
# Выключение pygame
pygame.quit()
