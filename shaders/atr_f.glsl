//GLSL
#version 140
in vec2 uv;
uniform sampler2D height_map;

vec3 get_normal(float terrain_height) {
  vec3 pixel_size = vec3(1.0, -1.0, 0) / textureSize(height_map,0).xxx;
  float u0 = texture(height_map, uv + pixel_size.yz).x * terrain_height;
  float u1 = texture(height_map, uv + pixel_size.xz).x * terrain_height;
  float v0 = texture(height_map, uv + pixel_size.zy).x * terrain_height;
  float v1 = texture(height_map, uv + pixel_size.zx).x * terrain_height;
  vec3 tangent = normalize(vec3(1.0, 0, u1 - u0));
  vec3 binormal = normalize(vec3(0, 1.0, v1 - v0));
  return normalize(cross(tangent, binormal));
}

void main()
    {
    float h=texture(height_map, uv).r;  
    vec3 n= get_normal(200.0);     
    vec3 up= vec3(0.0,0.0,1.0);
    
    float r1=(1.0-dot(n, up))*(1.0-h); //rock
    float b1=(1.0-r1)*(1.0-h); //grass
    float g1=(1.0-r1-b1); //dirt
      
    gl_FragData[0]=vec4(r1,g1,b1, 1.0); 
    }

