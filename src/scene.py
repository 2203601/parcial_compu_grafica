# Posiciona una cámara, administra los objetos y sus Graphics (VBO, VAO,
#ShaderProgram). Realiza transformaciones a los objetos que están en la escena y
#actualiza sus shaders. También actualiza viewport en on resize.
from graphics import Graphics
from raytracer import RayTracer
import glm
import math
import numpy as np
class Scene:
    def __init__(self, ctx, camera):
        self.ctx = ctx
        self.objects = []
        self.graphics = {} #objeto con shader
        self.camera = camera
        self.model = glm.mat4(1)
        self.view = camera.get_view_matrix()
        self.projection = camera.get_perspective_matrix()
        self.time = 0
        

    def add_object(self, model, material):
        self.objects.append(model)
        self.graphics[model.name] = Graphics(self.ctx, model, material)
    

    def render(self):
        self.time += 0.01
        #Rotar los objetos fuera del shader y actualizar sus matrices 
    
        for obj in self.objects:
            if(obj.name != "Sprite"):
                obj.rotation.x += 0.8 
                obj.rotation.y += 0.6 
                obj.rotation.z += 0.4 

                obj.position.x += math.sin(self.time) * 0.025
                obj.position.y += math.sin(self.time) * 0.001
                obj.position.z += math.sin(self.time) * 0.025

            model = obj.get_model_matrix()
            mvp = self.projection * self.view * model
            self.graphics[obj.name].render({'Mvp': mvp})
            self.graphics[obj.name].render({'pos_x': obj.position.x})


    def on_mouse_click(self, u, v):
        ray = self.camera.raycast(u,v)

        for obj in self.objects:
            if obj.check_hit(ray.origin, ray.direction):
                print(f"Golpeaste al objeto {obj.name}!")
                
    def on_resize(self, width, height):
        self.ctx.viewport = (0,0,width,height)
        self.camera.projection = glm.perspective(glm.radians(45),width/height, 0.1 , 100.0 )

    #depuracion
    def start(self):
        print("Start")

#es extender la funcionalidad de la escena base para que soporte raytracing utilizando un framebuffer.
class RayScene(Scene):
    def __init__(self, ctx, camera, width, height):
        super().__init__(ctx, camera)
        self.raytracer = RayTracer(camera,width,height)

    def start(self):
        self.raytracer.render_frame(self.objects)
        #busca el objeto con nombre "Sprite" y 
        # pide que actualice su textura con el contenido generado en el framebuffer.
        if "Sprite" in self.graphics:
            self.graphics["Sprite"].update_texture("u_texture", self.raytracer.get_texture())
        
    def render(self):
        super().render()

    #limpia el framebuffer, lo ajusta al nuevo tamaño de pantalla y 
    # ejecuta nuevamente start para redibujar el buffer con las dimensiones correctas.
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.raytracer = RayTracer(self.camera, width, height)
        self.start()