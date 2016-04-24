//GLSL
#version 140
in vec2 uv;
uniform sampler2D height_map;
uniform float erosion;
uniform float sharpness;

vec3 get_normal() {
  float terrain_height = 5.0;
  vec3 pixel_size = vec3(1.0, -1.0, 0) / textureSize(height_map,8).xxx;
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
    
    //blur
    float s=0.03*h;
    float blur = texture(height_map, uv+vec2( -0.326212, -0.405805)*s).r;
    blur += texture(height_map, uv + vec2(-0.840144, -0.073580)*s).r;
    blur += texture(height_map, uv + vec2(-0.695914, 0.457137)*s).r;
    blur += texture(height_map, uv + vec2(-0.203345, 0.620716)*s).r;
    blur += texture(height_map, uv + vec2(0.962340, -0.194983)*s).r;
    blur += texture(height_map, uv + vec2(0.473434, -0.480026)*s).r;
    blur += texture(height_map, uv + vec2(0.519456, 0.767022)*s).r;
    blur += texture(height_map, uv + vec2(0.185461, -0.893124)*s).r;
    blur += texture(height_map, uv + vec2(0.507431, 0.064425)*s).r;
    blur += texture(height_map, uv + vec2(0.896420, 0.412458)*s).r;
    blur += texture(height_map, uv + vec2(-0.321940, -0.932615)*s).r;
    blur += texture(height_map, uv + vec2(-0.791559, -0.597705)*s).r;    
    blur/=12.0;  
       
    h=mix(h,blur,sharpness);
    
    //erosion    
    vec3 up= vec3(0.0,0.0,1.0);
    vec3 n= get_normal();      
    float erode=mix(h, h*(h-(1.0-dot(n, up))), erosion);
    
    gl_FragData[0]=vec4(erode,0.0, 0.0, 1.0); 
    }

