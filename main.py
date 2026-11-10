import sys
import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

LARGURA = 800
ALTURA = 600


drone_pos = [0.0, 1.0, 0.0] 
drone_rot = 0.0 
helice_angulo = 0.0 
luz_ligada = True
celulas_coletadas = 0 
jogo_concluido = False


texturas = []


celulas = [
    [-4.0, 0.5, -5.0, True],
    [ 5.0, 0.5, -8.0, True],
    [-6.0, 0.5,-12.0, True],
    [ 4.0, 0.5,-15.0, True],
    [ 0.0, 0.5,-20.0, True]
]


obstaculos = [
    [-2.0, 0.5, -6.0, 1.5],
    [ 3.0, 0.5,-10.0, 2.0],
    [-1.0, 0.5,-16.0, 1.8]
]

def criar_textura_procedural(tipo):
    """Gera imagens proceduralmente para servir de textura sem depender de arquivos externos."""
    img_size = 64
    image = Image.new("RGB", (img_size, img_size))
    pixels = image.load()

    for x in range(img_size):
        for y in range(img_size):
            if tipo == "piso":
                
                if (x // 8 + y // 8) % 2 == 0:
                    pixels[x, y] = (50, 50, 60)
                else:
                    pixels[x, y] = (80, 80, 95)
            elif tipo == "caixa":
                
                if x < 4 or x > img_size - 5 or y < 4 or y > img_size - 5:
                    pixels[x, y] = (100, 100, 100)
                else:
                    pixels[x, y] = (140, 140, 140)

    # Converter imagem para formato compatível com OpenGL
    image_data = image.tobytes("raw", "RGB", 0, -1)
    
    text_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, text_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_size, img_size, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
    
    return text_id

def inicializar_opengl():
    global texturas
    pygame.init()
    pygame.display.set_mode((LARGURA, ALTURA), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Operação Resgate Orbital - CG")
    
    glViewport(0, 0, LARGURA, ALTURA)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (LARGURA / ALTURA), 0.1, 50.0)
    
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_TEXTURE_2D)

    
    luz_ambiente = [0.3, 0.3, 0.3, 1.0]
    luz_difusa = [0.8, 0.8, 0.8, 1.0]
    luz_posicao = [5.0, 10.0, 5.0, 1.0]
    
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    glLightfv(GL_LIGHT0, GL_POSITION, luz_posicao)


    texturas.append(criar_textura_procedural("piso"))   # Índice 0: Piso metálico
    texturas.append(criar_textura_procedural("caixa"))  # Índice 1: Caixa de manutenção

def desenhar_cubo(texture_id=None):
    if texture_id is not None:
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        rep = 4.0 if texture_id == texturas[0] else 1.0
        
        glBegin(GL_QUADS)
        
        glNormal3f(0.0, 0.0, 1.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5,  0.5)
        glTexCoord2f(rep, 0.0); glVertex3f( 0.5, -0.5,  0.5)
        glTexCoord2f(rep, rep); glVertex3f( 0.5,  0.5,  0.5)
        glTexCoord2f(0.0, rep); glVertex3f(-0.5,  0.5,  0.5)
        # Trás
        glNormal3f(0.0, 0.0, -1.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(rep, 0.0); glVertex3f(-0.5,  0.5, -0.5)
        glTexCoord2f(rep, rep); glVertex3f( 0.5,  0.5, -0.5)
        glTexCoord2f(0.0, rep); glVertex3f( 0.5, -0.5, -0.5)
        
        glNormal3f(0.0, 1.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5,  0.5, -0.5)
        glTexCoord2f(rep, 0.0); glVertex3f(-0.5,  0.5,  0.5)
        glTexCoord2f(rep, rep); glVertex3f( 0.5,  0.5,  0.5)
        glTexCoord2f(0.0, rep); glVertex3f( 0.5,  0.5, -0.5)
        # Base
        glNormal3f(0.0, -1.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(rep, 0.0); glVertex3f( 0.5, -0.5, -0.5)
        glTexCoord2f(rep, rep); glVertex3f( 0.5, -0.5,  0.5)
        glTexCoord2f(0.0, rep); glVertex3f(-0.5, -0.5,  0.5)
        
        glNormal3f(1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f( 0.5, -0.5, -0.5)
        glTexCoord2f(rep, 0.0); glVertex3f( 0.5,  0.5, -0.5)
        glTexCoord2f(rep, rep); glVertex3f( 0.5,  0.5,  0.5)
        glTexCoord2f(0.0, rep); glVertex3f( 0.5, -0.5,  0.5)
        
        glNormal3f(-1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(rep, 0.0); glVertex3f(-0.5, -0.5,  0.5)
        glTexCoord2f(rep, rep); glVertex3f(-0.5,  0.5,  0.5)
        glTexCoord2f(0.0, rep); glVertex3f(-0.5,  0.5, -0.5)
        glEnd()
    else:

        glDisable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glNormal3f(0.0, 0.0, 1.0)
        glVertex3f(-0.5, -0.5,  0.5); glVertex3f( 0.5, -0.5,  0.5); glVertex3f( 0.5,  0.5,  0.5); glVertex3f(-0.5,  0.5,  0.5)
        glNormal3f(0.0, 0.0, -1.0)
        glVertex3f(-0.5, -0.5, -0.5); glVertex3f(-0.5,  0.5, -0.5); glVertex3f( 0.5,  0.5, -0.5); glVertex3f( 0.5, -0.5, -0.5)
        glNormal3f(0.0, 1.0, 0.0)
        glVertex3f(-0.5,  0.5, -0.5); glVertex3f(-0.5,  0.5,  0.5); glVertex3f( 0.5,  0.5,  0.5); glVertex3f( 0.5,  0.5, -0.5)
        glNormal3f(0.0, -1.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5); glVertex3f( 0.5, -0.5, -0.5); glVertex3f( 0.5, -0.5,  0.5); glVertex3f(-0.5, -0.5,  0.5)
        glNormal3f(1.0, 0.0, 0.0)
        glVertex3f( 0.5, -0.5, -0.5); glVertex3f( 0.5,  0.5, -0.5); glVertex3f( 0.5,  0.5,  0.5); glVertex3f( 0.5, -0.5,  0.5)
        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5); glVertex3f(-0.5, -0.5,  0.5); glVertex3f(-0.5,  0.5,  0.5); glVertex3f(-0.5,  0.5, -0.5)
        glEnd()
        glEnable(GL_TEXTURE_2D)

def desenhar_drone():
    global helice_angulo
    glPushMatrix()
    glTranslatef(drone_pos[0], drone_pos[1], drone_pos[2])
    glRotatef(drone_rot, 0.0, 1.0, 0.0)


    glPushMatrix()
    glColor3f(0.2, 0.3, 0.4)
    glScalef(0.8, 0.3, 0.8)
    desenhar_cubo(None)
    glPopMatrix()


    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.45)
    glColor3f(0.9, 0.2, 0.2)
    glScalef(0.2, 0.2, 0.2)
    desenhar_cubo(None)
    glPopMatrix()


    offsets_bracos = [[0.6, 0.1, 0.6], [-0.6, 0.1, 0.6], [0.6, 0.1, -0.6], [-0.6, 0.1, -0.6]]
    
    for b in offsets_bracos:
        glPushMatrix()
        glTranslatef(b[0], b[1], b[2])
        
        
        glPushMatrix()
        glColor3f(0.5, 0.5, 0.5)
        glScalef(0.4, 0.1, 0.1)
        desenhar_cubo(None)
        glPopMatrix()


        glTranslatef(0.0, 0.1, 0.0)
        glRotatef(helice_angulo, 0.0, 1.0, 0.0)
        glColor3f(0.9, 0.9, 0.9)
        glScalef(0.6, 0.05, 0.15)
        desenhar_cubo(None)
        glPopMatrix()

    glPopMatrix()

def desenhar_cenario(tempo):

    glPushMatrix()
    glColor3f(1.0, 1.0, 1.0)
    glTranslatef(0.0, -0.5, 0.0)
    glScalef(30.0, 0.1, 50.0)
    desenhar_cubo(texturas[0])
    glPopMatrix()


    glColor3f(1.0, 1.0, 1.0)
    for obs in obstaculos:
        glPushMatrix()
        glTranslatef(obs[0], obs[1], obs[2])
        glScalef(obs[3], obs[3], obs[3])
        desenhar_cubo(texturas[1])
        glPopMatrix()


    for celula in celulas:
        if celula[3]:
            glPushMatrix()
            flutuar = math.sin(tempo * 3.0) * 0.1
            glTranslatef(celula[0], celula[1] + flutuar, celula[2])
            glRotatef(tempo * 50, 0.0, 1.0, 0.0)
            glColor3f(1.0, 0.8, 0.0)
            glScalef(0.4, 0.4, 0.4)
            desenhar_cubo(None)
            glPopMatrix()

    # Portal de Saída (Z = -25)[cite: 1, 2]
    glPushMatrix()
    glTranslatef(0.0, 1.5, -25.0)
    if celulas_coletadas >= 5:
        glColor3f(0.0, 1.0, 0.3) # Verde brilhante (Disponível)
    else:
        glColor3f(0.3, 0.3, 0.3) # Cinza escuro (Bloqueado)
    glScalef(2.0, 3.0, 0.5)
    desenhar_cubo(None)
    glPopMatrix()

def verificar_colisoes():
    global celulas_coletadas, jogo_concluido
    

    for celula in celulas:
        if celula[3]:
            dist = math.sqrt((drone_pos[0] - celula[0])**2 + (drone_pos[2] - celula[2])**2)
            if dist < 0.8:
                celula[3] = False
                celulas_coletadas += 1
                print(f"Célula coletada! Total: {celulas_coletadas}/5[cite: 4]")


    for obs in obstaculos:
        raio_colisao = (obs[3] / 2.0) + 0.4
        if abs(drone_pos[0] - obs[0]) < raio_colisao and abs(drone_pos[2] - obs[2]) < raio_colisao:
            return True


    if celulas_coletadas >= 5:
        if abs(drone_pos[0] - 0.0) < 1.5 and abs(drone_pos[2] - (-25.0)) < 1.0:
            if not jogo_concluido:
                jogo_concluido = True
                print("PARABÉNS! Missão concluída com sucesso! Pressione 'R' para reiniciar.")

    return False

def reiniciar_jogo():
    global drone_pos, drone_rot, celulas_coletadas, jogo_concluido, celulas
    drone_pos = [0.0, 1.0, 0.0]
    drone_rot = 0.0
    celulas_coletadas = 0
    jogo_concluido = False
    for celula in celulas:
        celula[3] = True
    print("Missão reiniciada!")

def main():
    global helice_angulo, luz_ligada, drone_pos
    inicializar_opengl()
    
    clock = pygame.time.Clock()
    tempo_acumulado = 0.0

    rodando = True
    while rodando:
        dt = clock.tick(60) / 1000.0
        tempo_acumulado += dt

        helice_angulo += 1000.0 * dt

        for evento in pygame.event.get():
            if evento.type == QUIT:
                rodando = False
            elif evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    rodando = False
                elif evento.key == K_l:
                    luz_ligada = not luz_ligada
                    if luz_ligada:
                        glEnable(GL_LIGHT0)
                    else:
                        glDisable(GL_LIGHT0)
                    print(f"Luz ligada: {luz_ligada}")
                elif evento.key == K_r:
                    reiniciar_jogo()

        teclas = pygame.key.get_pressed()
        velocidade = 5.0 * dt
        
        pos_antiga = list(drone_pos)

        if teclas[K_w]:
            drone_pos[2] -= velocidade
        if teclas[K_s]:
            drone_pos[2] += velocidade
        if teclas[K_a]:
            drone_pos[0] -= velocidade
        if teclas[K_d]:
            drone_pos[0] += velocidade

        if verificar_colisoes():
            drone_pos = pos_antiga

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        gluLookAt(drone_pos[0], drone_pos[1] + 2.5, drone_pos[2] + 5.0,
                drone_pos[0], drone_pos[1], drone_pos[2],
                0.0, 1.0, 0.0)

        desenhar_cenario(tempo_acumulado)
        desenhar_drone()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()