from panda3d.core import loadPrcFileData
loadPrcFileData("", "show-frame-rate-meter  0")
loadPrcFileData("", "sync-video 0")
loadPrcFileData("", "show-buffers 0")
loadPrcFileData("", "window-title  RAndom Terrain Generation UTility by wezu")
from direct.showbase.AppRunnerGlobal import appRunner
if appRunner: #run from binary/p3d
    path=appRunner.p3dFilename.getDirname()+'/'
else:  #run from python 
    path=''
from panda3d.core import *
from direct.showbase import ShowBase
from direct.gui.DirectGui import *
import random
import sys

class Demo():
    def __init__(self):       
        #setup
        self.size=1024
        self.edit_mode=False
        terrain_type='simple'        
        self.terrain_node=None 
        preset='hills'
        
        commands=sys.argv[1:]
        if '-res' in commands:
            try:
                self.size=int(commands[commands.index('-res')+1])
            except Exception as e:
                print e   
        if '-prev' in commands:
            try:
                terrain_type=commands[commands.index('-prev')+1]
            except Exception as e:
                print e 
        if '-edit' in commands:  
            self.edit_mode=True
        else:
            loadPrcFileData("", "window-type offscreen")  
        if '-preset' in commands:
            try:
                preset=commands[commands.index('-preset')+1]
            except Exception as e:
                print e 
                      
        base = ShowBase.ShowBase()
        if self.edit_mode:
            base.cam.set_pos(128, -128, 80)
            base.cam.look_at(128, 128, 0)
               
        self.height_map=self.make_buffer(Shader.load(Shader.SL_GLSL,'shaders/noise_v.glsl','shaders/noise_f.glsl'), self.size, rgbBits=(16, 0, 0, 0))
        
        self.erosion_map=self.make_buffer(Shader.load(Shader.SL_GLSL,'shaders/erode_v.glsl','shaders/erode_f.glsl'), self.size,rgbBits=(16, 0, 0, 0))
        self.erosion_map['quad'].set_shader_input('height_map', self.height_map['tex'])        
        
        self.atr_map=self.make_buffer(Shader.load(Shader.SL_GLSL,'shaders/atr_v.glsl','shaders/atr_f.glsl'), self.size,)
        self.atr_map['quad'].set_shader_input('height_map', self.erosion_map['tex'])
        
        #some starting inputs
        self.inputs={'seed1':random.random(),
                    'seed2':random.random(),
                    'seed3':random.random(),
                    'seed4':random.random(),
                    'seed5':random.random(),
                    'seed6':random.random()                    
                    }
        self.presets={
                    'moutains':{
                        'parm6': Vec2(21.5, 0.007),
                        'parm5': Vec2(1.2, -0.08),
                        'parm4': Vec2(1.95, 0.58),
                        'parm3': Vec2(1.58, -0.93),
                        'parm2': Vec2(7.4, 0.25),
                        'parm1': Vec2(1.85, 0.95),                   
                        'sharpness': [0.5],
                        'erosion': [0.4]
                        },
                    'hills':{
                        'parm3': LVector2f(1.15895, -0.93), 
                        'parm6': LVector2f(21.5, 0.0112105),
                        'parm5': LVector2f(1.2, -0.0315789),
                        'parm4': LVector2f(1.17807, 0.334386),
                        'parm3': LVector2f(1.15895, -0.93),       
                        'parm2': LVector2f(2.48772, 0.355263),
                        'parm1': LVector2f(0.902631, 0.957018),
                        'erosion': [0.4912281036376953],
                        'sharpness': [0.2719298005104065]
                        },
                    'dunes':{
                        'parm3': LVector2f(0.66772, 0.564737), 
                        'parm6': LVector2f(100, 0.00559648),
                        'parm5': LVector2f(1.2, -0.0119299),
                        'parm4': LVector2f(1.95, 0.334386), 
                        'parm2': LVector2f(0, 0.13772),
                        'parm1': LVector2f(0.130702, 0.599123),
                        'erosion': [0.9052631855010986],
                        'sharpness': [0.3070174753665924]    
                        },
                     'ridge':{
                        'parm3': LVector2f(0.842104, -0.221228),
                        'sharpness': [0.2175438106060028],
                        'parm6': LVector2f(1.75438, 0.0126141),
                        'parm5': LVector2f(0.350877, -0.0701754),
                        'parm4': LVector2f(0.491228, 0.15193),
                        'erosion': [0.9473683834075928],
                        'parm2': LVector2f(4.2807, 0.151754),
                        'parm1': LVector2f(0.376315, 0.852632)
                        },
                     'foothills':{
                        'parm3': LVector2f(0.210526, -0.375439),
                        'sharpness': [0.0],
                        'parm6': LVector2f(55.7895, 0.00770173),
                        'parm5': LVector2f(2.25263, 0.0126316),
                        'parm4': LVector2f(0.616668, 0.713333),
                        'erosion': [0.8631577491760254],
                        'parm2': LVector2f(1.71579, 0.579825),
                        'parm1': LVector2f(0.0605269, 0.621053)
                        },
                     'plains':{
                        'parm3': LVector2f(1.12281, 0.403334),
                        'sharpness': [1.0], 
                        'parm6': LVector2f(0.440877, 0.1),
                        'parm5': LVector2f(0.09, -0.1),
                        'parm4': LVector2f(1.12281, 0.341403),
                        'erosion': [0.23508775234222412],
                        'parm2': LVector2f(0.982455, 0.235965),
                        'parm1': LVector2f(0.105263, -0.522807)
                        },
                      'spikes':{
                            'parm3': LVector2f(1.58, -0.93),
                            'sharpness': [0.0],
                            'parm6': LVector2f(93.7807, -0.0063158),
                            'parm5': LVector2f(4.35789, 0.00491222),
                            'parm4': LVector2f(1.73947, 0.692281),
                            'erosion':[1.0],
                            'parm2': LVector2f(15.5403, 0.102631),
                            'parm1': LVector2f(1.85, 1)        
                        },
                      'canyon':{
                        'parm3': LVector2f(0.597547, -0.726316),
                        'sharpness': [0.0],
                        'parm6': LVector2f(1.50001, -0.0333333),
                        'parm5': LVector2f(0.881757, 0.0245614),
                        'parm4': LVector2f(1.04088, 0.880701),
                        'erosion': [1.0],
                        'parm2': LVector2f(1.57544, 1),
                        'parm1': LVector2f(1.21842, 1)
                        }      
                    }
        if preset in self.presets:
            self.inputs.update(self.presets[preset])
        else:
            self.inputs.update(self.presets['moutains'])    

        if self.edit_mode:
            #sliders        
            self.sliders=[]
            self.make_slider('parm1',0, [-0.8, 0.9],min_max=(0.0, 10.0))        
            self.make_slider('parm2',0, [-0.8, 0.8],min_max=(0.0, 20.0))
            self.make_slider('parm3',0, [-0.8, 0.7],min_max=(0.0, 20.0))
            self.make_slider('parm4',0, [-0.8, 0.6],min_max=(0.0, 20.0))
            self.make_slider('parm5',0, [-0.8, 0.5])
            self.make_slider('parm6',0, [-0.8, 0.4])
            
            self.make_slider('parm1',1, [0.3, 0.9], min_max=(-1.0, 1.0))
            self.make_slider('parm2',1, [0.3, 0.8], min_max=(-1.0, 1.0))
            self.make_slider('parm3',1, [0.3, 0.7], min_max=(-1.0, 1.0))
            self.make_slider('parm4',1, [0.3, 0.6], min_max=(-1.0, 1.0))
            self.make_slider('parm5',1, [0.3, 0.5], min_max=(-0.1, 0.1))
            self.make_slider('parm6',1, [0.3, 0.4], min_max=(-0.1, 0.1))
            
            self.make_slider('erosion',0, [-0.5, 0.3], min_max=(0.0, 1.0))
            self.make_slider('sharpness',0, [-0.5, 0.2], min_max=(0.0, 1.0))
            
            #save button
            self.save_button = DirectButton(text='SAVE',scale=0.1, pos=(-0.5,0.0,0.06), command=self.write )
            #reseed button
            self.save_button = DirectButton(text='RANDOM',scale=0.1, pos=(-0.5,0.0,-0.06), command=self.re_seed )
            
            self.preset_buttons=[]
            i=0
            for mode in self.presets:
                b=DirectButton(text=str(mode).upper(),scale=0.1, pos=(1.05,0.0,0.9-i*0.12), command=self.set_preset, extraArgs=[mode] )
                self.preset_buttons.append(b)
                i+=1
        else:
            self.send_inputs()
            base.graphicsEngine.renderFrame() 
            self.write()
            base.userExit()

        if terrain_type=='simple':
            self.terrain_node=None
            self.mesh=loader.loadModel('mesh/mesh80k')
            self.mesh.reparent_to(render)
            self.mesh.set_pos(-256, -256, -50)
            #shader
            terrain_shader=Shader.load(Shader.SL_GLSL, "shaders/terrain_v.glsl", "shaders/terrain_f.glsl")
            self.mesh.set_shader(terrain_shader)
            self.mesh.set_shader_input("height", self.erosion_map['tex'])
            self.mesh.set_shader_input("atr1", self.atr_map['tex'])
            self.mesh.set_shader_input("camera", base.camera)
            
            # Set some texture on the terrain
            grass_tex1 = base.loader.loadTexture("textures/grass.jpg")
            grass_tex1.set_minfilter(SamplerState.FT_linear_mipmap_linear)
            grass_tex1.set_anisotropic_degree(4)            
            dirt_tex1 = base.loader.loadTexture("textures/dirt.jpg")
            dirt_tex1.set_minfilter(SamplerState.FT_linear_mipmap_linear)
            dirt_tex1.set_anisotropic_degree(4)            
            rock_tex1 = base.loader.loadTexture("textures/rock.jpg")
            rock_tex1.set_minfilter(SamplerState.FT_linear_mipmap_linear)
            rock_tex1.set_anisotropic_degree(4)                        
            self.mesh.set_shader_input("grass1",grass_tex1)
            self.mesh.set_shader_input("dirt1",dirt_tex1)
            self.mesh.set_shader_input("rock1",rock_tex1)
            grass_tex1n = base.loader.loadTexture("textures/grass_n.jpg")
            grass_tex1n.set_minfilter(SamplerState.FT_linear_mipmap_linear)
            grass_tex1n.set_anisotropic_degree(4)            
            dirt_tex1n = base.loader.loadTexture("textures/dirt_n.jpg")
            dirt_tex1n.set_minfilter(SamplerState.FT_linear_mipmap_linear)
            dirt_tex1n.set_anisotropic_degree(4)            
            rock_tex1n = base.loader.loadTexture("textures/rock_n.jpg")
            rock_tex1n.set_minfilter(SamplerState.FT_linear_mipmap_linear)
            rock_tex1n.set_anisotropic_degree(4)                        
            self.mesh.set_shader_input("grass1n",grass_tex1n)
            self.mesh.set_shader_input("dirt1n",dirt_tex1n)
            self.mesh.set_shader_input("rock1n",rock_tex1n)
            
        elif terrain_type=='flat':
            cm = CardMaker("plane")
            cm.setFrame(0, 256, 0, 256)
            self.preview_plane=render.attachNewNode(cm.generate())
            self.preview_plane.setTexture(self.erosion_map['tex'])
            self.preview_plane.lookAt(0, 0, -1)     
            self.terrain_node=None
    
    def set_preset(self, mode):
        self.inputs.update(self.presets[mode])        
        for slider in self.sliders:
            name= slider['extraArgs'][1]
            index=slider['extraArgs'][2]
            slider['value']=self.inputs[name][index]
        
    def make_buffer(self, shader=None, size=256, rgbBits=(8, 8, 8, 0), mrt=False, texFilter=Texture.FTLinearMipmapLinear):
        root=NodePath("bufferRoot")
        tex=Texture()
        tex.set_wrap_u(Texture.WMClamp)
        tex.set_wrap_v(Texture.WMClamp)
        tex.set_magfilter(texFilter)
        tex.set_minfilter(texFilter)
        props = FrameBufferProperties()
        props.set_rgba_bits(rgbBits[0], rgbBits[1], rgbBits[2], rgbBits[3])
        props.set_srgb_color(False) 
        props.set_aux_rgba(mrt)             
        buff=base.win.make_texture_buffer("buff", size, size, tex, fbp=props)
        #the camera for the buffer
        cam=base.makeCamera(win=buff)
        cam.reparent_to(root)          
        cam.set_pos(size/2,size/2,100)                
        cam.set_p(-90)                   
        lens = OrthographicLens()
        lens.set_film_size(size, size)  
        cam.node().set_lens(lens)          
        #plane with the texture
        cm = CardMaker("plane")
        cm.set_frame(0, size, 0, size)        
        quad=root.attach_new_node(cm.generate())
        quad.look_at(0, 0, -1)      
        if shader:
            ShaderAttrib.make(shader)  
            quad.set_attrib(ShaderAttrib.make(shader))
        if mrt:
            aux_tex=Texture()
            aux_tex.set_wrap_u(Texture.WMClamp)
            aux_tex.set_wrap_v(Texture.WMClamp)
            aux_tex.set_magfilter(texFilter)
            aux_tex.set_minfilter(texFilter)
            buff.addRenderTexture(aux_tex, GraphicsOutput.RTMBindOrCopy, GraphicsOutput.RTPAuxRgba0)   
            return{'root':root, 'tex':tex, 'aux_tex':aux_tex,'buff':buff, "cam":cam, 'quad':quad}    
        #return all the data in a dict
        return{'root':root, 'tex':tex, 'buff':buff, "cam":cam, 'quad':quad}
    
        
    def make_slider(self, name, index, pos, min_max=(0.0, 100.0)):  
        value=self.inputs[name][index]          
        slider = DirectSlider(range=min_max, value=value, scale=0.5, pos=(pos[0],0.0,pos[1]), command=self.set_params)
        slider['extraArgs']=[slider,name, index]    
        self.sliders.append(slider)
        
    def re_seed(self):
        self.inputs['seed1']=random.random()
        self.inputs['seed2']=random.random()
        self.inputs['seed3']=random.random()
        self.inputs['seed4']=random.random()
        self.inputs['seed5']=random.random()
        self.inputs['seed6']=random.random()
        self.send_inputs()
        
    def write(self):
        p=PNMImage(self.size, self.size)              
        base.graphicsEngine.extract_texture_data(self.erosion_map['tex'],base.win.getGsg())
        self.erosion_map['tex'].store(p)
        #self.erosion_map['tex'].write("heightfield.png")
        p.write(path+"heightfield.png")        
        base.graphicsEngine.extract_texture_data(self.atr_map['tex'],base.win.getGsg())
        self.atr_map['tex'].store(p)
        p.write(path+"atr.png")    
        if self.terrain_node:
            self.terrain_node.generate()
        #print self.inputs
         
    def set_params(self, slider, name, index):     
        self.inputs[name][index]=float(slider['value'])
        #print name, index, slider['value']
        self.send_inputs()
        #self.write()
        
    def send_inputs(self):
        for key, value in self.inputs.items():
            if key not in ('erosion', 'sharpness'):
                self.height_map['quad'].set_shader_input(key, value)   
        
        self.erosion_map['quad'].set_shader_input('erosion',float(self.inputs['erosion'][0]))   
        self.erosion_map['quad'].set_shader_input('sharpness',float(self.inputs['sharpness'][0]))
d=Demo()
base.run()


