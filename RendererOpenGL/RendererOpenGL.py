import numpy as np
import imageio
import pygame
from pygame.locals import *
from gl import Renderer
from buffer import Buffer
from shaders import *
from model import Model
import glm
from PIL import Image
from OpenGL.GL import *  

# Configuración para la captura de fotogramas
capture_frames = True
frames = []
width, height = 272, 272  # Resolución ajustada para ser divisible por 16

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

# Inicialización del renderer y shaders
rend = Renderer(screen)
rend.SetShaders(vertex_shader, fragment_shader)

# Modelo y textura
faceModel = Model("models/model.obj")
faceModel.AddTexture("textures/model.bmp")
faceModel.rotation.y = 180
faceModel.translation.z = -5
faceModel.scale.x = 2
faceModel.scale.y = 2
faceModel.scale.z = 2

rend.scene.append(faceModel)
isRunning = True
frame_interval = 5  # Captura un fotograma cada 5 ciclos
frame_count = 0

# Revisa que el renderizador esté funcionando
rend.Render()
pygame.display.flip()

# Captura un fotograma de prueba
data = pygame.image.tostring(screen, 'RGB')
image = np.frombuffer(data, np.uint8).reshape((height, width, 3))
image = np.flip(image, axis=0)  # Voltear verticalmente para alinear la imagen
imageio.imwrite("test_frame.png", image)  # Guarda el primer fotograma como PNG para inspección

# Pausa para revisar el fotograma en PNG
print("Se guardó un fotograma de prueba como 'test_frame.png'. Revisa el archivo antes de continuar.")

# Continuar con el bucle principal si el fotograma de prueba se ve correctamente
while isRunning:
    deltaTime = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_1:
                rend.filledMode()
            elif event.key == pygame.K_2:
                rend.wireframeMode()
            elif event.key == pygame.K_3:
                rend.SetShaders(vertex_shader, fragment_shader)
            elif event.key == pygame.K_4:
                rend.SetShaders(ripple, fragment_shader)
            elif event.key == pygame.K_5:
                rend.SetShaders(twist, fragment_shader)
            elif event.key == pygame.K_6:
                rend.SetShaders(wave, fragment_shader)
            elif event.key == pygame.K_7:
                rend.SetShaders(pulse, fragment_shader)
            elif event.key == pygame.K_8:
                rend.SetShaders(vertex_shader, color)
            elif event.key == pygame.K_9:
                rend.SetShaders(vertex_shader, metallic)

    # Movimiento de cámara y modelo
    if keys[K_LEFT]:
        faceModel.rotation.y -= 10 * deltaTime
    if keys[K_RIGHT]:
        faceModel.rotation.y += 10 * deltaTime
    if keys[K_a]:
        rend.camera.position.x -= 1 * deltaTime
    if keys[K_d]:
        rend.camera.position.x += 1 * deltaTime
    if keys[K_w]:
        rend.camera.position.y += 1 * deltaTime
    if keys[K_s]:
        rend.camera.position.y -= 1 * deltaTime

    rend.time += deltaTime
    rend.Render()
    pygame.display.flip()

    # Captura de pantalla cada n fotogramas
    frame_data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (width, height), frame_data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)  
    frames.append(image)

pygame.quit()

imageio.mimsave('muestra.mp4', frames, fps=30)
