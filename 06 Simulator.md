# Simulator

[toc]

## Overview

The simulator of iGibson

- Maintain an instance of __Renderer__ and __PhysicsEngine__
- Can import __Scene, Object and Robot__

Key functions to use the simulator

- `load`: Initialize the physics engine and renderer
- `import_{scene, ig_scene}`: Import the scene into the simulator
- `import_{}`

## Examples

Import packages

    MAX_CLASS_COUNT = 512
    MAX_INSTANCE_COUNT = 1024

    import logging
    import os
    from sys import platform

    import numpy as np
    import yaml

    import igibson
    from igibson.envs.igibson_env import iGibsonEnv
    from igibson.external.pybullet_tools.utils import quat_from_euler
    from igibson.objects.articulated_object import URDFObject
    from igibson.objects.ycb_object import YCBObject
    from igibson.render.mesh_renderer.mesh_renderer_cpu import MeshRendererSettings
    from igibson.render.profiler import Profiler
    from igibson.robots.turtlebot import Turtlebot
    from igibson.scenes.empty_scene import EmptyScene
    from igibson.scenes.gibson_indoor_scene import StaticIndoorScene
    from igibson.simulator import Simulator
    from igibson.utils.assets_utils import get_ig_avg_category_specs, get_ig_category_path, get_ig_model_path
    from igibson.utils.utils import let_user_pick, parse_config

### Initialize the Simulator

Gibson simulator

    # Initialize Renderer Setting
    settings = MeshRendererSettings(
        enable_shadow=False, 
        msaa=False, 
        texture_scale=0.5
    )
    # Initialize the Simulator
    s = Simulator(
        # headless: have no viewer
        # gui_interactive: have a viewer
        mode = "gui_interactive",
        image_width=512,
        image_height=512,
        rendering_settings=settings,
    )
    # Set Viewing Position and Direction
    s.viewer.initial_pos = [-2, 1.4, 1.2]
    s.viewer.initial_view_direction = [0.6, -0.8, 0.1]
    s.viewer.reset_viewer()
    # End of Code, to Keep the Simulator Running
    try:
        max_steps = 10000
        for _ in range(max_steps):
            s.step()
    finally:
        s.disconnect()

iGibson simulator

### Load Scenes

Empty scene

    # Load an Empty Scene
    scene = EmptyScene(floor_plane_rgba=[0.6, 0.6, 0.6, 1])
    s.import_scene(scene)

Gibson scene

    # Load the Static Scene Rs
    scene = StaticIndoorScene("Rs", build_graph=True, pybullet_load_texture=False)
    s.import_scene(scene)

### Load Robots

    # Load a Turtlebot Robot
    config = parse_config(os.path.join(igibson.configs_path, "turtlebot_static_nav.yaml"))
    robot_config = config["robot"]
    robot_config.pop("name")
    turtlebot = Turtlebot(**robot_config)
    s.import_object(turtlebot)

### Load Objects

### Robot Actions

Control the robot to move and rotate

    try:
        max_steps = 10000
        for _ in range(max_steps):
            # The First Element Controls Movement
            # The Second Element Controls Rotation
            turtlebot.apply_action([1.0, 0.0])
            s.step()
    finally:
        s.disconnect()

Control the robot to render image
