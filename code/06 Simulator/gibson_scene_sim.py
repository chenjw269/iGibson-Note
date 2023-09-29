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
