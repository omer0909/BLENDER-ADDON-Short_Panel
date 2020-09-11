bl_info = {
    "name": "Short_Panel",
    "author": "Ömer Faruk Öz",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "PROPERTIES > Object > Hello World Panel",
    "description": "ShortWay",
    "warning": "",
    "doc_url": "",
    "category": "Interface",
}

import bpy

i=[]
def selectf(name):
    transformsobject=bpy.context.scene.objects
    
    for index in range(len(transformsobject)):
        if transformsobject[index].select_get():
            i.append(transformsobject[index].name)
    
    
    
    ob = bpy.context.scene.objects[name.name]
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True) 


def oldSelectf():
    
    transformsobject=bpy.context.scene.objects
    bpy.ops.object.select_all(action='DESELECT')
    for select in range(len(transformsobject)):
        for selected in range(len(i)):
            if i[selected]==transformsobject[select].name:
                z=bpy.context.scene.objects[transformsobject[select].name]
                z.select_set(True)
    i.clear()

def set(name):
    
    selectf(name)
    
    """area"""
    
    bpy.ops.object.duplicate ()
    newPlace=bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    
    """area"""
    
    oldSelectf()
                
    z=bpy.context.scene.objects[name.name]
    z.select_set(False)
    
    newPlace.select_set(True)
    
    
    return newPlace
    







#Unity Transform operator

def buttonunity(context):
    if  bpy.context.active_object.mode == 'OBJECT':
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        bpy.context.object.rotation_euler[1] = -1.5708
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        bpy.context.object.rotation_euler[1] = 1.5708
    







class UnityTransform(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.unity_transform"
    bl_label = "Unity Transform"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        buttonunity(context)
        return {'FINISHED'}



#droop operator

def buttondroop(context):
    if  bpy.context.active_object.mode == 'OBJECT' and bpy.context.view_layer.objects.active != None:
        if bpy.context.view_layer.objects.active.select_get():
            
            for object in bpy.context.selected_objects:
                if object == bpy.context.active_object:
                    oldplace=object.name
                    place=set(object)
                    for object in bpy.context.selected_objects:
                        if object != bpy.context.active_object:
                            oldRotationZ=object.rotation_euler.z
                            object.rotation_euler = (0,0,0)
                            constraint= object.constraints.new('SHRINKWRAP')
                            
                            constraint.shrinkwrap_type = 'PROJECT'
                            constraint.project_axis = 'NEG_Z'
                            constraint.target=place
                            constraint.use_track_normal = True
                            constraint.track_axis = 'TRACK_Z' 
                            selectf(object)
                            bpy.ops.object.visual_transform_apply()
                            oldSelectf()
                            
                            object.constraints.remove(constraint)
                            object.rotation_euler.rotate_axis("Z", oldRotationZ)
                            
                            
                            
                            
            ob = bpy.context.scene.objects[oldplace]
            bpy.context.view_layer.objects.active = ob
            ob.select_set(True) 
            
            objs = [bpy.context.scene.objects[place.name]]
            bpy.ops.object.delete({"selected_objects": objs})
                    
                    
                    
                    
                    


class Droop(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.droop"
    bl_label = "Droop"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        buttondroop(context)
        return {'FINISHED'}



#Denoise operator 


def buttondenois(context):
    
    bpy.context.scene.use_nodes = True
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.view_layer.cycles.denoising_store_passes = True
    
    
    scene = bpy.context.scene
    
    nodetree = scene.node_tree
    
    node1 = nodetree.nodes.new("CompositorNodeDenoise")

    
    node2 = nodetree.nodes.new("CompositorNodeRLayers")
    node2.location = (-300,0)
    
    
    for a in nodetree.nodes:
        if a.type == 'COMPOSITE':
            node0=a
    
    
    nodetree.links.new(node2.outputs[3],node1.inputs[0])
    nodetree.links.new(node2.outputs[4],node1.inputs[1])
    nodetree.links.new(node2.outputs[5],node1.inputs[2])
    nodetree.links.new(node1.outputs[0],node0.inputs[0])
    



class Denoiseshot(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.denoiseshot"
    bl_label = "Denoise"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        buttondenois(context)
        return {'FINISHED'}

#Set Orgin operator 

def buttonorgin(context):
    if bpy.context.active_object.mode == 'EDIT':
        cursor=(bpy.context.scene.cursor.location.x,bpy.context.scene.cursor.location.y,bpy.context.scene.cursor.location.z)
        
        area=bpy.context.area.type
        bpy.context.area.type = 'VIEW_3D'
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.context.area.type = area
        bpy.ops.object.editmode_toggle()
        
        selectf(bpy.context.active_object)
        visible=[]
        modifierList = bpy.context.object.modifiers.keys()
        
        for modifier in modifierList:
            if bpy.context.object.modifiers[modifier].show_viewport ==True:
                visible.append(True)
                bpy.context.object.modifiers[modifier].show_viewport = False
            else:
                visible.append(False)
           
           
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        
        
        for index in range(len(modifierList)):
            if visible[index]:
                bpy.context.object.modifiers[modifierList[index]].show_viewport = True
        oldSelectf()
        
        bpy.ops.object.editmode_toggle()
        
        bpy.context.scene.cursor.location=cursor
        





class Orgin(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.orgin"
    bl_label = "Set Orgin"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        buttonorgin(context)
        return {'FINISHED'}





class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Short Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        #obj = context.object

        #row = layout.row()
        #row.label(text="Hello world!", icon='WORLD_DATA')

        #row = layout.row()
        #row.label(text="Active object is: " + obj.name)
        #row = layout.row()
        #row.prop(obj, "name")

        row = layout.row()
        row.operator("object.unity_transform")
        
        row = layout.row()
        row.operator("object.droop")
        
        row = layout.row()
        row.operator("object.denoiseshot")
        
        row = layout.row()
        row.operator("object.orgin")
        
        
        
def register():
    bpy.utils.register_class(UnityTransform)
    bpy.utils.register_class(Droop)
    bpy.utils.register_class(Denoiseshot)
    bpy.utils.register_class(Orgin)
    bpy.utils.register_class(HelloWorldPanel)


def unregister():
    bpy.utils.unregister_class(UnityTransform)
    bpy.utils.unregister_class(Droop)
    bpy.utils.unregister_class(Denoiseshot)
    bpy.utils.unregister_class(Orgin)
    bpy.utils.unregister_class(HelloWorldPanel)


if __name__ == "__main__":
    register()
