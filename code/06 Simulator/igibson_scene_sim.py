import os
from sys import platform

import numpy as np

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
