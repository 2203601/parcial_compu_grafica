#carga de shaders
from moderngl import Attribute, Uniform
import numpy as np
import glm

class ShaderProgram:
    def __init__(self, ctx, vertex_shader_path, fragment_shader_path):
        with open(vertex_shader_path) as file:
            vertex_shader = file.read()
        with open(fragment_shader_path) as file:
            fragment_shader = file.read()

        self.prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        attributes = []
        uniforms = []

        for name in self.prog:
            member = self.prog[name]
            if type(member) is Attribute:
                attributes.append(name)
            if type(member) is Uniform:
                uniforms.append(name)
        
        self.attributes = list(attributes)
        self.uniforms = uniforms
   
   
   
   
    def set_uniform(self, name, value):
        if name  in self.uniforms:
            uniform = self.prog[name]
            # Caso matriz (ej: glm.mat4 convertido a np.array)
            if isinstance(value, glm.mat4):
                uniform.write(value.to_bytes())
            # Caso float
            elif hasattr(uniform, "value"):
                uniform.value = value


        # Caso glm (ej: glm.mat4 o glm.vec3)
        else:
            try:
                arr = np.array(value, dtype='f4')
                self.prog[name].write(arr.tobytes())
            except Exception as e:
                print(f"Could not set uniform {name}: {e}")