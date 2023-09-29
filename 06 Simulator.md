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

### Load Scene

Use simulator in Gibson scene

    from sys import platform

    from igibson.render.mesh_renderer.mesh_renderer_settings import MeshRendererSettings
    from igibson.render.profiler import Profiler
    from igibson.scenes.gibson_indoor_scene import StaticIndoorScene
    from igibson.simulator import Simulator


    settings = MeshRendererSettings(enable_shadow=True, msaa=False)
    if platform == "darwin":
        settings.texture_scale = 0.5
    s = Simulator(
        mode="gui_interactive",
        image_width=512,
        image_height=512,
        rendering_settings=settings,
    )

    # Choose scene id
    scene_list = [
        "Rs"
    ]
    scene_id = "Rs"
    scene = StaticIndoorScene(
        scene_id,
        # load_object_categories=[],  # To load only the building. Fast
        build_graph=True,
    )
    s.import_scene(scene)

    # Set a better viewing direction
    s.viewer.initial_pos = [-2, 1.4, 1.2]
    s.viewer.initial_view_direction = [0.6, -0.8, 0.1]
    s.viewer.reset_viewer()

    # Keep simulator running
    max_steps = 1000
    step = 0
    while step != max_steps:
        with Profiler("Simulator step"):
            s.step()
            step += 1
        
    s.disconnect()

Use simulator in iGibson scene

    from sys import platform

    from igibson.render.mesh_renderer.mesh_renderer_settings import MeshRendererSettings
    from igibson.render.profiler import Profiler
    from igibson.scenes.igibson_indoor_scene import InteractiveIndoorScene
    from igibson.simulator import Simulator


    settings = MeshRendererSettings(enable_shadow=True, msaa=False)
    if platform == "darwin":
        settings.texture_scale = 0.5
    s = Simulator(
        mode="gui_interactive",
        image_width=512,
        image_height=512,
        rendering_settings=settings,
    )

    # Choose scene id
    scene_list = [
        "Beechwood_0_int", "Beechwood_1_int",
        "Benevolence_0_int", "Benevolence_1_int", "Benevolence_2_int",
        "Ihlen_0_int", "Ihlen_1_int",
        "Merom_0_int", "Merom_1_int",
        "Pomaria_0_int", "Pomaria_1_int", "Pomaria_2_int",
        "Rs_int",
        "Wainscott_0_int", "Wainscott_1_int"
    ]
    scene_id = "Rs_int"
    scene = InteractiveIndoorScene(
        scene_id,
        # load_object_categories=[],  # To load only the building. Fast
        build_graph=True,
    )
    s.import_scene(scene)

    # Set a better viewing direction
    s.viewer.initial_pos = [-2, 1.4, 1.2]
    s.viewer.initial_view_direction = [0.6, -0.8, 0.1]
    s.viewer.reset_viewer()

    # Keep simulator running
    max_steps = 1000
    step = 0
    while step != max_steps:
        with Profiler("Simulator step"):
            s.step()
            step += 1
        
    s.disconnect()

Use environment in Gibson scene

Use environment in iGibson scene

    MAX_CLASS_COUNT = 512
    MAX_INSTANCE_COUNT = 1024

    import os
    from sys import platform
    import yaml

    import igibson
    from igibson.envs.igibson_env import iGibsonEnv
    from igibson.render.profiler import Profiler


    # Read scene config
    config_filename = os.path.join(igibson.configs_path, "turtlebot_nav.yaml")
    config_data = yaml.load(open(config_filename, "r"), Loader=yaml.FullLoader)
    config_data["load_object_categories"] = []  # Uncomment this line to accelerate loading with only the building
    config_data["visible_target"] = False
    config_data["visible_path"] = False

    # Choose scene id
    scene_list = [
        "Beechwood_0_int", "Beechwood_1_int",
        "Benevolence_0_int", "Benevolence_1_int", "Benevolence_2_int",
        "Ihlen_0_int", "Ihlen_1_int",
        "Merom_0_int", "Merom_1_int",
        "Pomaria_0_int", "Pomaria_1_int", "Pomaria_2_int",
        "Rs_int",
        "Wainscott_0_int", "Wainscott_1_int"
    ]
    config_data["scene_id"] = "Beechwood_0_int"

    # Reduce texture scale for Mac.
    if platform == "darwin":
        config_data["texture_scale"] = 0.5
    env = iGibsonEnv(config_file=config_data, mode="gui_interactive")
    s = env.simulator

    # Set a better viewing direction
    s.viewer.initial_pos = [-2, 1.4, 1.2]
    s.viewer.initial_view_direction = [0.6, -0.8, 0.1]
    s.viewer.reset_viewer()

    # Keep simulator running
    try:
        env.reset()
        for i in range(100):
            with Profiler("Environment action step"):
                # action = env.action_space.sample()
                state, reward, done, info = env.step([0.1, 0.1])
                if done:
                    print("Episode finished after {} timesteps".format(i + 1))
                    break  
    finally:
        env.close()

### Load Robots

Load a turtlebot robot from file config

    from igibson.robots.turtlebot import Turtlebot
    from igibson.utils.utils import parse_config

    # Load a Turtlebot Robot
    config = parse_config(os.path.join(igibson.configs_path, "turtlebot_static_nav.yaml"))
    robot_config = config["robot"]
    robot_config.pop("name")
    turtlebot = Turtlebot(**robot_config)
    s.import_object(turtlebot)

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

### Load Objects
