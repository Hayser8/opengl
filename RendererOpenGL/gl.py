import glm 
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from camera import Camera
from skybox import *

class Renderer(object): 
    def __init__(self, screen):
        self.screen = screen
        _,_ , self.width, self.height = screen.get_rect()
        
        glClearColor(0.2, 0.2,0.2, 1)

        glEnable(GL_DEPTH_TEST)
        glViewport(0,0, self.width, self.height)

        self.camera = Camera(self.width, self.height)
        self.time = 0
        self.value = 0
        self.pointLight = glm.vec3(0,0,0)
        self.scene= []
        self.active_shaders = None

        # SkyBox != EnvMap

        self.skybox = None

    def CreateSkybox(self, textureList, vShader, fShader):
        self.skybox = Skybox(textureList, vShader, fShader)

    def FilledMode(self): 
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
    def WireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def SetShaders(self, vShader, fShader):
        if vShader is not None and fShader is not None: 
            self.active_shaders = compileProgram( compileShader(vShader, GL_VERTEX_SHADER), 
                                                  compileShader(fShader, GL_FRAGMENT_SHADER)) 
        else: 
            self.active_shaders= None
            

        
    
    def Render(self): 
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.skybox is not None:
            self.skybox.Render(self.camera.GetViewMatrix(), self.camera.GetProjectionMatrix())
        if self.active_shaders is not None: 
            glUseProgram(self.active_shaders) 
            
            glUniform1f(glGetUniformLocation(self.active_shaders, "time") , self.time)
        
            glUniformMatrix4fv(glGetUniformLocation(self.active_shaders, "viewMatrix"), #ubicacion
                                          1, GL_FALSE, #matrices
                                          glm.value_ptr(self.camera.GetViewMatrix() )) #pointer

            glUniformMatrix4fv(glGetUniformLocation(self.active_shaders, "projectionMatrix"), #ubicacion
                                          1, GL_FALSE, #matrices
                                          glm.value_ptr(self.camera.GetProjectionMatrix() )) #pointer
            
            glUniform3fv(glGetUniformLocation(self.active_shaders, "pointLight"), 1, glm.value_ptr(self.pointLight))

            
        for obj in self.scene:
            if self.active_shaders is not None: 
                glUniformMatrix4fv(glGetUniformLocation(self.active_shaders, "modelMatrix"), #ubicacion
                                          1, GL_FALSE, #matrices
                                          glm.value_ptr(obj.GetModelMatrix() ) #pointer
                                         )
            
                obj.Render()
    
