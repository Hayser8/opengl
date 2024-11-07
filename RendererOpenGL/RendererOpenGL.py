import pygame
from pygame.locals import *
from OpenGL.GL import *  
from gl import Renderer
from buffer import *
from shaders import *
from model import *
import glm
import imageio
from PIL import Image

# Configuración de pantalla
screen_width = 540
screen_height = 540

pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.OPENGL | pygame.DOUBLEBUF) 

clock = pygame.time.Clock()

renderer = Renderer(screen)

# Texturas de la skybox
skybox_textures = [
    "skybox/right.jpg",
    "skybox/left.jpg",
    "skybox/top.jpg",
    "skybox/bottom.jpg",
    "skybox/front.jpg",
    "skybox/back.jpg"
]

renderer.CreateSkybox(skybox_textures, skybox_vertex_shader, skybox_fragment_shader)

# Modelo OBJ
model = Model("models/Monkey.obj")
model.AddTexture("textures/MonkeyDiffuse.bmp")
model.translation.z = -5
model.translation.y = -1  
model.scale = glm.vec3(2, 2, 2)

renderer.scene.append(model)

# Variables de control
is_running = True

vertex_shader_program = vertex_shader
fragment_shader_program = fragment_shader

# Configuración de la cámara
camera_distance = 7  
camera_angle = 0
camera_height = 0
camera_max_distance = 20  
camera_min_distance = 3   
camera_max_height = 7
camera_min_height = -7

renderer.SetShaders(vertex_shader_program, fragment_shader_program)

frames = []

while is_running: 
    delta_time = clock.tick(60) / 1000.0
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_ESCAPE:
                is_running = False
            if event.key == pygame.K_1:
                renderer.FilledMode()
            if event.key == pygame.K_2:
                renderer.WireframeMode()
            if event.key == pygame.K_3:
                vertex_shader_program = fat_shader
                renderer.SetShaders(vertex_shader_program, fragment_shader_program)
            if event.key == pygame.K_4:
                vertex_shader_program = water_shader
                renderer.SetShaders(vertex_shader_program, fragment_shader_program)
            if event.key == pygame.K_5:
                vertex_shader_program = wave
                renderer.SetShaders(vertex_shader_program, fragment_shader_program)
            if event.key == pygame.K_6:
                vertex_shader_program = pulse
                renderer.SetShaders(vertex_shader_program, fragment_shader_program)
            if event.key == pygame.K_7:
                fragment_shader_program = color
                renderer.SetShaders(vertex_shader_program, fragment_shader_program)   
            if event.key == pygame.K_8:
                fragment_shader_program = metallic
                renderer.SetShaders(vertex_shader_program, fragment_shader_program)                   

    # Movimiento de la luz
    if keys[K_LEFT]:
        renderer.pointLight.x -= 1 * delta_time
    
    if keys[K_RIGHT]:
        renderer.pointLight.x += 1 * delta_time

    if keys[K_UP]:
        camera_height = min(camera_max_height, camera_height + 2 * delta_time)
    
    if keys[K_DOWN]:
        camera_height = max(camera_min_height, camera_height - 2 * delta_time)

    if keys[K_PAGEUP]:
        renderer.pointLight.y += 1 * delta_time
    
    if keys[K_PAGEDOWN]:
        renderer.pointLight.y -= 1 * delta_time

    # Movimiento de la cámara
    if keys[K_a]:
        camera_angle -= 45 * delta_time

    if keys[K_d]:
        camera_angle += 45 * delta_time

    if keys[K_w]:
        camera_distance = max(camera_min_distance, camera_distance - 2 * delta_time)

    if keys[K_s]:
        camera_distance = min(camera_max_distance, camera_distance + 2 * delta_time)

    # Actualización de la escena
    renderer.time += delta_time

    renderer.camera.LookAt(model.translation)
    renderer.camera.Orbit(model.translation, camera_distance, camera_angle, camera_height)
    renderer.Render()
    pygame.display.flip()

    # Captura de cuadros para video
    frame_data = glReadPixels(0, 0, screen_width, screen_height, GL_RGB, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (screen_width, screen_height), frame_data)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)  
    frames.append(image)

pygame.quit()

# Guardado de video
imageio.mimsave('output.mp4', frames, fps=30)
