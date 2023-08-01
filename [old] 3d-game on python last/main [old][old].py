# Импорт pygame и остальных библиотек
import pygame
from os import path
import math

# Константы
WxH = [800, 600]
FPS = 30
running = True # Цикл работы окна
FOV = 60 # Угол обзора в градусах

# Импорт изображений
img_dir = path.join(path.dirname(__file__), 'img')

# Инициализация pygame
pygame.init()
# Создание окна
screen = pygame.display.set_mode(WxH)
pygame.display.set_caption("Test ray-casting")
clock = pygame.time.Clock()
#font_name = pygame.font.match_font('arial')

# Характеристики игрового поля
# Массив точек стен
points = [[100, 100], [100, 200], [200, 100],
          [200, 200], [140, 140], [160, 160]]
# Массив стен через точки
walls = [[0, 1], [0, 2], [1, 3], [2, 3], [4, 5]]

# Функции
# Нахлждение растояния до стены (новая)
def wallcross(p1, ang, p3, p4):    
    # Нахождение промежуточной точки
    p2 = [(p1[0] - 50 * math.sin(math.radians(ang))),
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

            # Проверка возможности такой стены
            if dst != 0:
                return (5*WxH[1] / dst)  #// math.cos(math.radians((ply.rot+ang) // 2 )))

            else:
                return WxH[1]
        else:         
            #pygame.draw.circle(screen, (255, 255, 0), (cx, cy), 5)
            return 0
    else:
        return 0

    
# Отрисовка стены
def walldraw(h, cycle, dH):
    # Проверка возможности отрисовки
    t = h*2
    if t > 255:
        t = 255
    # Отрисовка стены
    pygame.draw.line(screen, (0, 0, t), (cycle, WxH[1]//2-h+dH), (cycle, WxH[1]//2+h+dH))

    # Кайма сверху
    pygame.draw.line(screen, (0, 0, 0), (cycle, WxH[1]//2-h+dH+2), (cycle, WxH[1]//2-h+dH))

    # Кайма снизу
    pygame.draw.line(screen, (0, 0, 0), (cycle, WxH[1]//2+h+dH-2), (cycle, WxH[1]//2+h+dH))
    

    
# Класс игрока
class player(pygame.sprite.Sprite):
    def __init__(self, X, Y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.orig_img = pygame.transform.scale(plyimg, (16, 16))
        self.image = self.orig_img
        #self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = X
        self.rect.centery = Y
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
            self.speedy = 2
        if keystate[pygame.K_a]:
            self.speedy = -2

        if keystate[pygame.K_LSHIFT]:
            self.speedx *= 2
            self.speedy *= 2

        # Изменение угла благодаря курсору
        self.rot = int(self.rot + (WxH[0]//2 - pygame.mouse.get_pos()[0])/2) % 360

        # Возврат курсора в изночальное положение
        pygame.mouse.set_pos((WxH[0]//2, WxH[1]//2))

        sinx = round(math.sin(math.radians(self.rot)), 1)
        cosx = round(math.cos(math.radians(self.rot)), 1)

        # Изменение координаты в зависимости от угла и нажатия клавиш
        self.rect.x += self.speedx * sinx
        self.rect.x -= self.speedy * cosx

        self.rect.y -= self.speedx * cosx
        self.rect.y -= self.speedy * sinx

        self.speedx = 0
        self.speedy = 0

# Загрузка графики
plyimg = pygame.image.load(path.join(img_dir, "player-image.png")).convert()

wallimg = pygame.image.load(path.join(img_dir, "1.png")).convert()


# Группа спрайтов для отрисовки
all_sprites  = pygame.sprite.Group()

# Создание объектов в мире
# Создание игрока
ply = player(140, 160, 270);
all_sprites.add(ply)

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
    
    # Обновление
    all_sprites.update()

    # Рендеринг
    # Запоняем экран цветом неба
    screen.fill((0, 255, 255))

    # Отрисовка иллюзии пола
    pygame.draw.rect(screen, (127, 127, 127), ((0, WxH[1]//2), (WxH[0], WxH[1])))

    # Отрисовка псевдо-трёхмерных стен
    for i in range(WxH[0]+1):
        # Нахождение пересечения со стеной
        dst = [] # Список расстояний до стен
        ang = i*FOV/WxH[0] - FOV//2 - ply.rot # Угол просчёта

        # Нахождение пересечений со стенами
        for j in walls:
            c = wallcross(ply.rect.center, ang, points[j[0]], points[j[1]])
            if c != 0:
                dst.append(c)
                
        # Отрисовка стены
        if (dst != []) and (min(dst) != 0):
            walldraw(max(dst), i, 0)

    # Отрисовка миникарты для отладки
    for i in walls:
        # Отрисовка стен
        pygame.draw.line(screen, (127, 127, 127), points[i[0]], points[i[1]])

    # Отрисовка игрока
    pygame.draw.circle(screen, (0, 0, 0), ply.rect.center, 5)
    # Отрисовка поля зрения
    pygame.draw.line(screen, (128, 128, 128), (ply.rect.centerx, ply.rect.centery),
                     ((ply.rect.centerx+30*math.sin(math.radians(ply.rot-FOV//2))),
                      (ply.rect.centery-30*math.cos(math.radians(ply.rot-FOV//2)))))
    pygame.draw.line(screen, (128, 128, 128), (ply.rect.centerx, ply.rect.centery),
                     ((ply.rect.centerx+30*math.sin(math.radians(ply.rot+FOV//2))),
                      (ply.rect.centery-30*math.cos(math.radians(ply.rot+FOV//2)))))

    pygame.draw.line(screen, (128, 128, 128), ply.rect.center,
                     ((ply.rect.centerx+30*math.sin(math.radians(ply.rot))),
                      (ply.rect.centery-30*math.cos(math.radians(ply.rot)))))
    
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
    
# Выключение pygame
pygame.quit()
