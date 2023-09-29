# Scenes

[toc]

## Overview

Provide four types of scenes

- `EmptyScene` and `StadiumScene`: simple scenes with flat grounds and no obstacles, useful for debugging purposes
- `StaticIndoorScene`: loads static 3D scenes from `igibson.g_dataset_path`.
- `InteractiveIndoorScene`: loads fully interactive 3D scenes from `igibson.ig_dataset_path`

Scene types take in the `scene_id` of a scene and provide a `load` function that be invoked externally (usually by `import_scene` of the `Simulator`)

The `load` function of `StaticIndoorScene`

## Adding other scenes

## Examples

### Stadium Scenes

### Static Building Scenes

### Interactive Building Scenes

### Random Positions

Gibson simulator

iGibson simulator

    import logging
    from sys import platform

    import numpy as np

    from igibson.render.mesh_renderer.mesh_renderer_settings import MeshRendererSettings
    from igibson.render.profiler import Profiler
    from igibson.scenes.igibson_indoor_scene import InteractiveIndoorScene
    from igibson.simulator import Simulator


    scene_id = "Rs_int"
    settings = MeshRendererSettings(enable_shadow=True, msaa=False)
    if platform == "darwin":
        settings.texture_scale = 0.5
    s = Simulator(
        mode="gui_interactive",
        image_width=512,
        image_height=512,
        rendering_settings=settings,
    )

    scene = InteractiveIndoorScene(
        scene_id,
        # load_object_categories=[],  # To load only the building. Fast
        build_graph=True,
    )
    s.import_scene(scene)

    # Shows how to sample points in specific room
    np.random.seed(0)
    for _ in range(10):
        pt = scene.get_random_point_by_room_type("living_room")[1]
        print("Random point in living_room: {}".format(pt))

    # Shows how to sample trajectories in total floor
    for _ in range(10):
        random_floor = scene.get_random_floor()
        p = scene.get_random_point(random_floor)[1]
        print("Random point: {}".format(p))

    max_steps = 1000
    step = 0
    while step != max_steps:
        with Profiler("Simulator step"):
            s.step()
            step += 1

    s.disconnect()

### Random Trajectories

Gibson simulator

iGibson simulator
