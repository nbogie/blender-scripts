bl_info = {
    "name": "Make Object Cluster",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import random #from random import randint, random, gauss, randrange, sample
import colorsys # for hsv to rgb colour conversion
import mathutils














    
# TODO: don't pollute global namespace w these utility fns

# take a single function and call it three times to create a tuple: (a, b, c)
# useful for creating vectors for rotation, position, location, scaling, etc, based on the same function.
def triple(fn):
    return (fn(), fn(), fn())


def rgb255PaletteToBlender(inPalette):
    return [(r/100, g/100, b/100, 1) for (r, g, b) in inPalette]


def random_colour():
    return (random.random(), random.random(), random.random(), 1)


def random_pastel_colour():    
    r, g, b = colorsys.hsv_to_rgb(random.random(), 0.9, 0.7)
    return (r, g, b, 1)


def random_colour_from_palette():
    #source: https://www.colourlovers.com/palette/443995/i_demand_a_pancake
    palette = rgb255PaletteToBlender([(89,79,79), (84,121,128), (69,173,168), (157,224,173), (229,252,194)])
    chosen = random.sample(palette, 1)
    return chosen[0]

def create_one_object(center_pos, context):
    pos = triple(lambda: random.gauss(0, 10))
    pos = mathutils.Vector(pos) + mathutils.Vector(center_pos)

    scaling = triple(lambda: random.gauss(10, 5))
    rotation = triple(lambda: random.randrange(0, 360, 45))
    rotation = (0,0,0)

    #create a cube!
    bpy.ops.mesh.primitive_cube_add(size=1, align='WORLD', location=pos, rotation=rotation)

    #set scale
    created = bpy.context.view_layer.objects.active
    created.scale = scaling
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=False)

    #set material
    mat = bpy.data.materials.new(name="MaterialName")
    mat.diffuse_color = random_colour_from_palette() #or try random_pastel_colour()
    created.data.materials.append(mat)        

    #subdivide
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=5)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #add a modifier
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    bpy.context.object.modifiers["SimpleDeform"].deform_method="TAPER"
    bpy.context.object.modifiers["SimpleDeform"].deform_axis=random.choice(['X', 'Y', 'Z'])
    bpy.context.object.modifiers["SimpleDeform"].factor=random.random()*0.4 - 0.2
    

        

def create_cluster(center_pos, context):
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    num_objects_to_create=10
    for i in range(num_objects_to_create):
        create_one_object(center_pos, context)
        
    for obj in context.scene.objects:
        obj.location.x += 1.0


print("new load")

class MakeObjectCluster(bpy.types.Operator):
    """Neill's Object Cluster Creation Script"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.make_cluster"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Make Object Cluster"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    @classmethod
    def poll(cls, context):
        return bpy.context.object.mode != None and bpy.context.object.mode == 'OBJECT'
        #and active_nobject is not None
    
    def execute(self, context):        # execute() is called when running the operator.
        center_pos = context.scene.cursor.location
        create_cluster(center_pos, context)
        return {'FINISHED'}            # Lets Blender know the operator finished successfully.

def register():
    bpy.utils.register_class(MakeObjectCluster)


def unregister():
    bpy.utils.unregister_class(MakeObjectCluster)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
    
