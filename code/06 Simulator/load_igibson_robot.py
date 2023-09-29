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

from igibson.robots.turtlebot import Turtlebot
from igibson.utils.utils import parse_config

# Load a Turtlebot Robot
config = parse_config(os.path.join(igibson.configs_path, "turtlebot_static_nav.yaml"))
robot_config = config["robot"]
robot_config.pop("name")
turtlebot = Turtlebot(**robot_config)
s.import_object(turtlebot)

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
            turtlebot.apply_action([1.0, 0.0])
            if done:
                print("Episode finished after {} timesteps".format(i + 1))
                break  
finally:
    env.close()