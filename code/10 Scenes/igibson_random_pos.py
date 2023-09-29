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

# Shows how to sample points in the scene
np.random.seed(0)
for _ in range(10):
    pt = scene.get_random_point_by_room_type("living_room")[1]
    print("Random point in living_room: {}".format(pt))

# Shows how to sample trajectories in the scene
for _ in range(10):
    random_floor = scene.get_random_floor()
    p1 = scene.get_random_point(random_floor)[1]
    p2 = scene.get_random_point(random_floor)[1]
    shortest_path, geodesic_distance = scene.get_shortest_path(random_floor, p1[:2], p2[:2], entire_path=True)
    print("Random point 1: {}".format(p1))
    print("Random point 2: {}".format(p2))
    print("Geodesic distance between p1 and p2: {}".format(geodesic_distance))
    print("Shortest path from p1 to p2: {}".format(shortest_path))


max_steps = 1000
step = 0
while step != max_steps:
    with Profiler("Simulator step"):
        s.step()
        step += 1

s.disconnect()
