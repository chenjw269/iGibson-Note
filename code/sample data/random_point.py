import os
import logging
from sys import platform

import numpy as np

from igibson.render.mesh_renderer.mesh_renderer_settings import MeshRendererSettings
from igibson.render.profiler import Profiler
from igibson.scenes.igibson_indoor_scene import InteractiveIndoorScene
from igibson.simulator import Simulator
from igibson.utils.assets_utils import get_available_ig_scenes


def random_point(simulator, pth):
    
    

def main():
    
    bs_pth = "D:/Workspace/Datasets/iGibson" # Path to save data
    sample_nums = 500 # Samples number
    house_id = 1 # Choos house identifier
    
    # House identifier map
    id_name_dict = {
        1: "Beechwood_0_int",
        2: "Beechwood_1_int",
        3: "Benevolence_0_int",
        4: "Benevolence_1_int",
        5: "Benevolence_2_int",
        6: "Ihlen_0_int",
        7: "Ihlen_1_int",
        8: "Merom_0_int",
        9: "Merom_1_int",
        10: "Pomaria_0_int",
        11: "Pomaria_1_int",
        12: "Pomaria_2_int",
        13: "Rs_int",
        14: "Wainscott_0_int",
        15: "Wainscott_1_int"
    }
    
    # Initialize a simulator
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
        id_name_dict[house_id],
        load_object_categories=[],  # To load only the building. Fast
        build_graph=True,
    )
    s.import_scene(scene)

    # Sample random points
    np.random.seed(0)
    points = []
    for _ in range(1000):
        random_floor = scene.get_random_floor()
        p1 = scene.get_random_point(random_floor)[1]
        points.append(p1)


def get_first_options():
    return get_available_ig_scenes()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()