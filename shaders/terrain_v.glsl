//GLSL
#version 140
in vec2 p3d_MultiTexCoord0;
in vec4 p3d_Vertex;
in vec3 p3d_Normal;

uniform sampler2D height;
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat4 p3d_ModelMatrix;

out vec2 terrain_uv;
out vec4 world_pos;;


void main()
    {        
    float h= textureLod(height, p3d_MultiTexCoord0, 0.0).r;   
    vec4 vert=p3d_Vertex;
    vert.z=h*100.0; 
    gl_Position = p3d_ModelViewProjectionMatrix * vert;      
          
    world_pos=p3d_ModelMatrix* vert;         
    terrain_uv=p3d_MultiTexCoord0;
    }
