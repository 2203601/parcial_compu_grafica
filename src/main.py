#ejecuta el programa, crea un ventana window, un shaderprogram
#una scene, crea las instancias de los objetivos graficos (cube)
#crea la camra y la posiciona
#agrega los objetos en la escena y corre el loop principal

from window import Window
from texture import Texture
from material import Material
from shader_program import ShaderProgram
from cube import Cube
from camera import Camera
from scene import Scene, RayScene
from quad import Quad
import numpy as np

WIDTH, HEIGHT = 800,600
# ventana
window = Window(WIDTH, HEIGHT, "Basic Grapphic Engine")

# shader
shader_program = ShaderProgram(window.ctx , 'shaders/basic.vert', 'shaders/basic.frag')
shader_program_skybox = ShaderProgram(window.ctx , 'shaders/sprite.vert', 'shaders/sprite.frag')


# textura
skybox_texture = Texture(width=WIDTH, height=HEIGHT,channels_amount=3, color=(0,0,0) )

material = Material(shader_program)
material_sprite = Material(shader_program_skybox, textures_data=[skybox_texture])

#objetos
cube1 = Cube ((-2,0,2), (0,45,0), (1,1,1), name="Cube1")
cube2 = Cube ((2,0,2), (0,45,0), (1,1,1), name="Cube2")
quad = Quad((0,0,0), (0,0,0), (6,5,1), name="Sprite", hittable = False)

# camara
camera = Camera((0,0,10), (0,0,0), (0,1,0), 45, window.width / window.height, 0.1, 100.0)

#escena
scene = RayScene(window.ctx, camera, WIDTH, HEIGHT)

scene.add_object(cube1, material)
scene.add_object(cube2, material)
scene.add_object(quad, material_sprite)

#carga de la escena y ejecución del loop principal

window.set_scene(scene)
window.run()

