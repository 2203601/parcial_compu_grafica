//  inyección de codigo en el render  pipeline de la gpu que gestiona
// cada pixel generando en la rasterizacion de un objeto poligonal
// siempre debe devolver un vec4 de color (r,g,b,a) donde a es transparencia

#version 330

in vec3 v_color;
out vec4 f_color;

void main(){
   f_color = vec4(v_color,1.0);
}
