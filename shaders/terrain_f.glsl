#version 150

in vec2 terrain_uv;
in vec4 world_pos;;

out vec4 color;

uniform sampler2D height;
uniform sampler2D atr1;
uniform sampler2D grass1;
uniform sampler2D dirt1;
uniform sampler2D rock1;
uniform sampler2D grass1n;
uniform sampler2D dirt1n;
uniform sampler2D rock1n;
uniform vec3 wspos_camera;

// Compute normal from the heightmap, this assumes the terrain is facing z-up
vec3 get_terrain_normal() {
  const float terrain_height = 50.0;
  vec3 pixel_size = vec3(1.0, -1.0, 0) / textureSize(height, 0).xxx;
  float u0 = texture(height, terrain_uv + pixel_size.yz).x * terrain_height;
  float u1 = texture(height, terrain_uv + pixel_size.xz).x * terrain_height;
  float v0 = texture(height, terrain_uv + pixel_size.zy).x * terrain_height;
  float v1 = texture(height, terrain_uv + pixel_size.zx).x * terrain_height;
  vec3 tangent = normalize(vec3(1.0, 0, u1 - u0));
  vec3 binormal = normalize(vec3(0, 1.0, v1 - v0));
  return normalize(cross(tangent, binormal));
}



void main() {
    vec3 mask1=texture(atr1, terrain_uv).xyz;  
    vec3 diffuse = texture(rock1, terrain_uv * 16.0).xyz*mask1.g;
    diffuse += texture(dirt1, terrain_uv * 16.0).xyz*mask1.r;
    diffuse += texture(grass1, terrain_uv * 16.0).xyz*mask1.b;
      
    //vec3 normal = get_terrain_normal();
    
    //normal vector...
    vec3 vLeft=vec3(1.0,0.0,0.0);                 
    vec3 up= vec3(0.0,0.0,1.0);
    vec3 norm=vec3(0.0,0.0,1.0);    
    vec4 me=texture(height,terrain_uv);
    float pixel=1.0/textureSize(height, 0).x;
    vec4 n=texture(height, vec2(terrain_uv.x,terrain_uv.y+pixel)); 
    vec4 s=texture(height, vec2(terrain_uv.x,terrain_uv.y-pixel));   
    vec4 e=texture(height, vec2(terrain_uv.x+pixel,terrain_uv.y));    
    vec4 w=texture(height, vec2(terrain_uv.x-pixel,terrain_uv.y));
    //find perpendicular vector to norm:        
    vec3 temp = norm; //a temporary vector that is not parallel to norm    
    temp.x+=0.5;
    //form a basis with norm being one of the axes:
    vec3 perp1 = normalize(cross(norm,temp));
    vec3 perp2 = normalize(cross(norm,perp1));
    //use the basis to move the normal in its own space by the offset                       
    norm -= 50.0*(((n.r-me.r)-(s.r-me.r))*perp1 - ((e.r-me.r)-(w.r-me.r))*perp2);
    vec3 N = normalize(norm); 
    
    vec4 norm_map = vec4(0.0,0.0,0.0,0.0);
            norm_map+=texture(dirt1n, terrain_uv * 16.0)*mask1.r;
            norm_map+=texture(rock1n, terrain_uv * 16.0)*mask1.g;
            norm_map+=texture(grass1n, terrain_uv * 16.0)*mask1.b;    
    norm_map=norm_map*2.0-1.0;
    vec3 tangent=  cross(N, vLeft);  
    vec3 binormal= cross(N, tangent); 
    N.xyz *= norm_map.z;
    N.xyz += tangent * norm_map.x;
    N.xyz += binormal * norm_map.y;  
    N = normalize(N);        
    
    

    // Add some fake lighting - you usually want to use your own lighting code here
    vec3 fake_sun = normalize(vec3(0.7, 0.2, 0.6));  
    vec3 shading = max(0.0, dot(N, fake_sun)) * diffuse;
    shading += vec3(0.1, 0.1, 0.1);

    color = vec4(shading, 1.0);
}
