import pygame;
from Icon import interface
import random
import math
from pygame import mixer


# Initialize pygame
pygame.init()

#Screen size

pantalla = pygame.display.set_mode((800, 600))
fondo = pygame.image.load('Fondo.jpg')

se_ejecuta = True
# imagen jugador
img_jugador = pygame.image.load('astronave.png')

#colocar sonido
mixer.music.load('MusicaFondo.mp3')
mixer.music.play()
# inicializa el punto de partida
lado_X = 368
lado_Y =532
jugador_control =0

# texto final del juego
fuenteFinal = pygame.font.Font('freesansbold.ttf',32)
def textoFinal():
    mi_fuenteFinal = fuenteFinal.render('Juego Terminado', True,(255,255,255))
    pantalla.blit(mi_fuenteFinal,(300,200))


#Lista de enemigos
img_enemy = []
enemy_X = []
enemy_Y = []
enemy_cambia_X =[]
enemy_cambia_Y =[]
cantidad_enemigos = 8
# imagen enemigo
for e in range(cantidad_enemigos):
    img_enemy.append(pygame.image.load('enemigo.png'))
    enemy_X.append(random.randint(0,732))
    enemy_Y.append(random.randint(50,200))
    enemy_cambia_X.append(0.3) 
    enemy_cambia_Y.append(50)


# Bala
img_bala = pygame.image.load('bala.png')
bala_X = 0
bala_Y = 532
bala_Cambia_X = 0
bala_Cambia_Y =1
bala_visible = False

# puntaje
puntaje = 0

fuente = pygame.font.Font('freesansbold.ttf',32)
texto_X = 10
texto_Y = 10


#mostrar Puntaje
def mostrarPuntaje(x,y):
    texto = fuente.render(f'Puntaje {puntaje}', True, (255,255,255))
    pantalla.blit(texto,(x,y))
# Funcion del jugador
def jugador(x,y):
    pantalla.blit(img_jugador, (x,y))
# Funcion del enemigo    

def enemigo(x,y,ene):

    pantalla.blit(img_enemy[ene], (x,y))  

def bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala,(x,y))

def detectarColision(x1,y1,x2,y2):
    distancia = math.sqrt(math.pow(x1-x2, 2) + math.pow(y2-y1,2))
    if distancia <27:
        return True
    else:
        return False    

# interfaz
interface()
while se_ejecuta == True:
    # color de fondo de pantalla
    pantalla.blit(fondo, (0,0))
    # eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_control = -0.3
            if evento.key == pygame.K_RIGHT:
                jugador_control = 0.3
            #Movimiento de bala
            if evento.key == pygame.K_SPACE:
                musica_bala = mixer.Sound('disparo.mp3')
                musica_bala.play()
                if not bala_visible:
                    bala_X = lado_X
                    bala(bala_X, bala_Y)   
                
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_control = 0    

    # Modificacion de la ubicacion                        
    lado_X += jugador_control

    # mantener dentro del area
    if lado_X <=0:
        lado_X =0
    elif lado_X >=732:
        lado_X = 732   

    # modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):
        # fin del juego
        if enemy_Y[e]>532:
            for k in range(cantidad_enemigos):
                enemy_Y[k]= 1000
            textoFinal()
            break
                
        enemy_X[e] += enemy_cambia_X[e]
        # manter dentro del area el enemigo
        if enemy_X[e] <=0:
            enemy_cambia_X[e] = 0.3
            enemy_Y[e] +=enemy_cambia_Y[e]
       
        elif enemy_X[e] >= 732:
            enemy_cambia_X[e] = -0.3
            enemy_Y[e] +=enemy_cambia_Y[e]
        #colision
        colision = detectarColision(enemy_X[e], enemy_Y[e], bala_X, bala_Y)
        if colision:
            sonido_colosion = mixer.Sound('Golpe.mp3')
            sonido_colosion.play()
            bala_Y = 532
            bala_visible = False
            puntaje +=1
            enemy_X[e] = random.randint(0,732)
            enemy_Y[e] = random.randint(50,200)
            print(puntaje)   
        enemigo(enemy_X[e], enemy_Y[e],e)      
    
    enemy_X += enemy_cambia_X
  
    #Reset bala 
    if bala_Y <=0:
        bala_Y = 532
        bala_visible = False
    # bala 
    if bala_visible:
        bala(bala_X, bala_Y)
        bala_Y -= bala_Cambia_Y
        
    mostrarPuntaje(texto_X, texto_Y)
    jugador(lado_X, lado_Y)
   
    # actualizar
    pygame.display.update()
