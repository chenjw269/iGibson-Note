import os
from sys import platform

import numpy as np

from igibson.render.mesh_renderer.mesh_renderer_settings import MeshRendererSettings
from igibson.render.profiler import Profiler
from igibson.scenes.igibson_indoor_scene import InteractiveIndoorScene
from igibson.simulator import Simulator


def sample_image(scene_id, output_pth, nums):

    if not os.path.exists(f"{output_pth}/{scene_id}"):
        os.makedirs(f"{output_pth}/{scene_id}")

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

    # Sample random points
    np.random.seed(0)

    points_list = []
    for _ in range(nums):
        random_floor = scene.get_random_floor()
        p = scene.get_random_point(random_floor)[1]
        print("Random point: {}".format(p))
        points_list.append(p)

        renderer = s.renderer
        

    # fp = open(f"{output_pth}/{scene_id}/pose.txt", "w")
    # for p in points_list:
    #     fp.write(f"{round(p[0], 4)}, {round(p[1], 4)}\n")
        
    max_steps = 5
    step = 0
    while step != max_steps:
        with Profiler("Simulator step"):
            s.step()
            step += 1
        
    s.disconnect()
     

if __name__ == "__main__":

    scene_list = [
        "Beechwood_0_int", "Beechwood_1_int",
        "Benevolence_0_int", "Benevolence_1_int", "Benevolence_2_int",
        "Ihlen_0_int", "Ihlen_1_int",
        "Merom_0_int", "Merom_1_int",
        "Pomaria_0_int", "Pomaria_1_int", "Pomaria_2_int",
        "Rs_int",
        "Wainscott_0_int", "Wainscott_1_int"
    ]

    output_pth = "D:/Workspace/Datasets/iGibson-v0/"
    nums = 10

    for scene_id in scene_list:
        sample_image(scene_id, output_pth, nums)
