# Renderer

[toc]

## Overview

The MeshRenderer of iGibson

- Supports __customizable camera configuration__ and
- Supports __various image modalities__
- Renders at a __lightening speed__

Key functions to use the renderer

- `class MeshRenderer`: Specify image width, height and vertical field of view
- `renderer.render(modes=('rgb', 'normal', 'seg', '3d', 'optical_flow', 'scene_flow'))`: Retrieve the images

## Examples

### Use Renderer

Gibson simulator

    import logging
    import os
    import sys

    import cv2
    import numpy as np

    from igibson.render.mesh_renderer.mesh_renderer_cpu import MeshRenderer
    from igibson.utils.assets_utils import get_scene_path


    model_path = os.path.join(get_scene_path("Rs"), "mesh_z_up.obj")

    renderer = MeshRenderer(width=512, height=512)
    renderer.load_object(model_path)
    renderer.add_instance_group([0])
    camera_pose = np.array([0, 0, 1.2])
    view_direction = np.array([1, 0, 0])
    renderer.set_camera(camera_pose, camera_pose + view_direction, [0, 0, 1])
    renderer.set_fov(90)
    frames = renderer.render(modes=("rgb", "normal", "3d"))

    # Render 3d points as depth map
    depth = np.linalg.norm(frames[2][:, :, :3], axis=2)
    depth /= depth.max()
    frames[2][:, :, :3] = depth[..., None]

    frames = cv2.cvtColor(np.concatenate(frames, axis=1), cv2.COLOR_RGB2BGR)
    cv2.imshow("image", frames)
    cv2.waitKey(0)

iGibson simulator

### Interactive Renderer

### Multi Sensors

Render a frame with specific modals

    # RGB, Normal and 3d Images Store in a List
    frames = renderer.render(modes=("rgb", "normal", "3d"))

Visualize / Save RGB image

    rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    # Visualize RGB image
    cv2.imshow("RGB image", rgb)
    # Save RGB image
    cv2.imwrite("rgb.jpg", rgb)

Visualize / Save depth image

    depth = frames[2]
    depth_cp = np.linalg.norm(depth[:, :, :3], axis=2)
    depth_cp /= depth_cp.max()
    depth[:, :, :3] = depth_cp[..., None]
    depth = depth * 255
    # Visualize depth image
    cv2.imshow("Depth image", depth)
    # Save depth image
    cv2.imwrite("depth.jpg", depth)

Process segmentation image

- Mode `seg` and `ins_seg` provides a 4-channeled image, the first channel corresponds to the segmentation result
- The values are normalized between 0 and 1, with a normalizing constant of `MAX_CLASS_COUNT = 512` and `MAX_INSTANCE_COUNT = 1024`


        [seg, ins_seg] = renderer.render(modes=('seg', 'ins_seg'))
        seg = (seg[:, :, 0:1] * MAX_CLASS_COUNT).astype(np.int32)
        ins_seg = (ins_seg[:, :, 0:1] * MAX_INSTANCE_COUNT).astype(np.int32)

- Map the segmentation result to image

        # Render semantic segmentation result
        MAX_CLASS_COUNT = 512
        seg = (seg[:, :, 0:1] * MAX_CLASS_COUNT).astype(np.int32)
        colors = matplotlib.cm.get_cmap("plasma", 16)
        seg_img = np.squeeze(colors(seg), axis=2) * 255
        cv2.imwrite(f"Segment image.jpg", seg_img)

        # Render instance segmentation result
        MAX_INSTANCE_COUNT = 1024
        ins_seg = (ins_seg[:, :, 0:1] * MAX_INSTANCE_COUNT).astype(np.int32)
        colors = matplotlib.cm.get_cmap("plasma", 16)
        ins_seg_img = np.squeeze(colors(ins_seg), axis=2) * 255
        cv2.imwrite(f"Instance Segment image.jpg", ins_seg_img)