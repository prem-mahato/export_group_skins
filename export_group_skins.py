# -*- coding: utf-8 -*-

"""
Author: Prem Kumar Mahato
LinkedIn: www.linkedin.com/in/premkumarmahato
ArtStation: https://www.artstation.com/premkumarmahato8
Last Updated: 22/03/2025
Version: 1.0

About: Export and Import Group Skin in Maya.
"""

import maya.cmds as cmds
import json
import os

# ==============================================================================
# UTILS
# ==============================================================================

def get_skin_cluster(mesh):
    history = cmds.listHistory(mesh) or []
    skins = cmds.ls(history, type='skinCluster')
    
    if skins:
        return skins[0]
        
    return None


def get_meshes_from_groups(groups):
    meshes = []
    
    for grp in groups:
        shapes = cmds.listRelatives(
            grp,
            ad=True,
            type='mesh',
            fullPath=True
        ) or []
        
        for shape in shapes:
            try:
                if cmds.getAttr(shape + ".intermediateObject"):
                    continue
            except:
                pass
                
            parent = cmds.listRelatives(
                shape,
                p=True,
                fullPath=True
            )
            
            if parent:
                meshes.append(parent[0])
                
    return list(set(meshes))


# ==============================================================================
# EXPORT
# ==============================================================================

def export_skin_from_groups(file_path):
    groups = cmds.ls(sl=True, long=True)
    
    if not groups:
        cmds.error("Select at least one group.")
        
    meshes = get_meshes_from_groups(groups)
    
    if not meshes:
        cmds.error("No meshes found.")
        
    export_data = {}
    
    for mesh in meshes:
        skin_cluster = get_skin_cluster(mesh)
        
        if not skin_cluster:
            continue
            
        influences = cmds.skinCluster(
            skin_cluster,
            q=True,
            influence=True
        ) or []
        
        vtx_count = cmds.polyEvaluate(mesh, vertex=True)
        
        mesh_data = {
            "mesh": mesh,
            "skinCluster": skin_cluster,
            "vertexCount": vtx_count,
            "influences": influences,
            "weights": {}
        }
        
        print("Exporting: " + mesh)
        
        for vtx_id in range(vtx_count):
            vertex = "%s.vtx[%d]" % (mesh, vtx_id)
            influence_data = {}
            
            for inf in influences:
                try:
                    weight = cmds.skinPercent(
                        skin_cluster,
                        vertex,
                        transform=inf,
                        q=True
                    )
                    
                    if weight > 0.0:
                        influence_data[inf] = weight
                        
                except:
                    pass
                    
            mesh_data["weights"][str(vtx_id)] = influence_data
            
        export_data[mesh] = mesh_data
        
    f = open(file_path, "w")
    json.dump(export_data, f, indent=4)
    f.close()
    
    print("")
    print("==========================================")
    print("Skin Export Complete")
    print(file_path)
    print("==========================================")


# ==============================================================================
# IMPORT
# ==============================================================================

def import_skin(file_path):

    if not os.path.exists(file_path):
        cmds.error("File does not exist: " + file_path)

    f = open(file_path, "r")
    data = json.load(f)
    f.close()

    for mesh in data.keys():

        if not cmds.objExists(mesh):
            cmds.warning("Mesh not found: " + mesh)
            continue

        mesh_data = data[mesh]

        influences = mesh_data["influences"]

        missing = []

        for j in influences:
            if not cmds.objExists(j):
                missing.append(j)

        if missing:

            cmds.warning(
                "Missing joints on %s : %s"
                % (
                    mesh,
                    ", ".join(missing),
                )
            )
            continue

        existing_skin = get_skin_cluster(mesh)

        if existing_skin:
            try:
                cmds.delete(existing_skin)
            except:
                pass

        print("Creating skinCluster: " + mesh)

        skin_cluster = cmds.skinCluster(
            influences,
            mesh,
            tsb=True,
            nw=1,
        )[0]

        weights_data = mesh_data["weights"]

        total_vtx = mesh_data["vertexCount"]

        for vtx_id in range(total_vtx):

            vertex = "%s.vtx[%d]" % (
                mesh,
                vtx_id,
            )

            key = str(vtx_id)

            if key not in weights_data:
                continue

            influence_values = []

            for joint, weight in weights_data[key].items():

                influence_values.append(
                    (
                        joint,
                        weight,
                    )
                )

            if influence_values:

                try:
                    cmds.skinPercent(
                        skin_cluster,
                        vertex,
                        transformValue=influence_values,
                    )
                except:
                    pass

        cmds.skinCluster(
            skin_cluster,
            e=True,
            forceNormalizeWeights=True,
        )

        print("Imported: " + mesh)

    print("")
    print("==========================================")
    print("Skin Import Complete")
    print("==========================================")


# ==============================================================================
# BROWSE SAVE FILE
# ==============================================================================

def export_skin_ui():

    result = cmds.fileDialog2(
        fileMode=0,
        caption="Export Skin Data",
        fileFilter="JSON (*.json)",
    )

    if result:
        export_skin_from_groups(result[0])


def import_skin_ui():

    result = cmds.fileDialog2(
        fileMode=1,
        caption="Import Skin Data",
        fileFilter="JSON (*.json)",
    )

    if result:
        import_skin(result[0])


# ==============================================================================
# USAGE
# ==============================================================================

# Select one or more groups
# export_skin_ui()

# Import
# import_skin_ui()

# Or direct path:

# export_skin_from_groups("D:/skinData.json")
# import_skin("D:/skinData.json")