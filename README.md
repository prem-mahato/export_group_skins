# Maya Export / Import Group Skin

A Python tool for Autodesk Maya that allows you to export and import skin weights for all skinned meshes inside selected groups.

## About

This tool exports skin data from meshes inside selected groups and saves the information as a JSON file.

The exported data can later be imported to recreate the `skinCluster` and restore the vertex skin weights.

## Features

- Export skin weights from one or multiple groups.
- Automatically find meshes inside selected groups.
- Detect `skinCluster` on each mesh.
- Export influencing joints.
- Export per-vertex skin weights.
- Save skin data as JSON.
- Import previously exported skin data.
- Recreate the `skinCluster`.
- Restore vertex weights.
- Support multiple skinned meshes.

## How To Use
```python
# Select one or more groups
export_skin_ui()

# Import
import_skin_ui()

# Or direct path:

export_skin_from_groups("D:/skinData.json")
import_skin("D:/skinData.json")
```

## Use Case

One use case is preparing a character skeleton for Unreal Engine.

For example, while creating a skeleton mesh for UE, the rig may need to be scaled and the joint transforms frozen. In this situation, the skin can be temporarily removed and restored after the skeleton operation.

```text
Character Rig
      |
      v
Export Group Skin
      |
      v
Remove Skin
      |
      v
Scale / Freeze Skeleton
      |
      v
Prepare Skeleton for Unreal Engine
      |
      v
Import Group Skin
      |
      v
Restore Skin Weights
