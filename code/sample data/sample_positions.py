import logging
import os
from sys import platform

import numpy as np
import yaml
import cv2
import matplotlib

import igibson
from igibson.envs.igibson_env import iGibsonEnv
from igibson.render.profiler import Profiler


def sample_data(simulator, index, pth):
    
    rgb, seg, depth, ins_seg = simulator.renderer.render_robot_cameras(modes=("rgb", "seg", "3d", "ins_seg"))
    
    rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    rgb = rgb * 255
    cv2.imwrite(f"{pth}/rgb/{index}.jpg", rgb)
    
    MAX_CLASS_COUNT = 512
    seg = (seg[:, :, 0:1] * MAX_CLASS_COUNT).astype(np.int32)
    colors = matplotlib.cm.get_cmap("plasma", 16)
    seg_img = np.squeeze(colors(seg), axis=2) * 255
    cv2.imwrite(f"{pth}/seg/{index}.jpg", seg_img)
    np.save(f"{pth}/seg/{index}.npy", seg)
    
    depth_cp = np.linalg.norm(depth[:, :, :3], axis=2)
    depth_cp /= depth_cp.max()
    depth[:, :, :3] = depth_cp[..., None]
    depth = depth * 255
    cv2.imwrite(f"{pth}/depth/{index}.jpg", depth)
    
    MAX_INSTANCE_COUNT = 1024
    ins_seg = (ins_seg[:, :, 0:1] * MAX_INSTANCE_COUNT).astype(np.int32)
    colors = matplotlib.cm.get_cmap("plasma", 16)
    ins_seg_img = np.squeeze(colors(ins_seg), axis=2) * 255
    # cv2.imwrite(f"{pth}/ins_seg/{index}.jpg", ins_seg_img)
    # np.save(f"{pth}/ins_seg/{index}.npy", ins_seg_img)
    
    return


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
    
    # Read sampling positions
    pose_pth = f"{bs_pth}/{id_name_dict[house_id]}/pose.txt"
    poses = []
    with open(pose_pth) as f:
        for fl in f:
            fl = fl[:-1].split(",")
            poses.append([eval(fl[0]), eval(fl[1]), 0.5])
    poses = poses[:sample_nums]

    # Check whether the path is available
    is_folder = os.path.exists(f"{bs_pth}/{id_name_dict[house_id]}/gt")
    if not is_folder:
        os.makedirs(f"{bs_pth}/{id_name_dict[house_id]}/gt")
    is_folder = os.path.exists(f"{bs_pth}/{id_name_dict[house_id]}/rgb")
    if not is_folder:
        os.makedirs(f"{bs_pth}/{id_name_dict[house_id]}/rgb")
    is_folder = os.path.exists(f"{bs_pth}/{id_name_dict[house_id]}/depth")
    if not is_folder:
        os.makedirs(f"{bs_pth}/{id_name_dict[house_id]}/depth")
    is_folder = os.path.exists(f"{bs_pth}/{id_name_dict[house_id]}/seg")
    if not is_folder:
        os.makedirs(f"{bs_pth}/{id_name_dict[house_id]}/seg")
    is_folder = os.path.exists(f"{bs_pth}/{id_name_dict[house_id]}/ins_seg")
    if not is_folder:
        os.makedirs(f"{bs_pth}/{id_name_dict[house_id]}/ins_seg")

    # Initialize a simulator
    config_filename = os.path.join(igibson.configs_path, "turtlebot_nav.yaml")
    config_data = yaml.load(open(config_filename, "r"), Loader=yaml.FullLoader)
    # config_data["load_object_categories"] = []  # Uncomment this line to accelerate loading with only the building
    config_data["visible_target"] = False
    config_data["visible_path"] = False
    config_data["scene_id"] = id_name_dict[house_id]

    env = iGibsonEnv(
        config_file=config_data,
        mode="gui_interactive"
    )
    s = env.simulator

    s.viewer.initial_pos = [-0.3, 0.5, 1.2]
    s.viewer.initial_view_direction = [0.9, -0.3, -0.2]
    s.viewer.reset_viewer()

    # Sample data
    try:
        print("Resetting environment")
        env.reset()
        
        for i in range(len(poses)):
            
            env.reset()
            
            with Profiler("Environment action step"):
                
                # Step process
                state, reward, done, info = env.step([0.0, 0.0])
                
                # Set simulator in i-th position
                env.robots[0].set_position(poses[i]) 

                # Sample with z axis rotating 0 degree
                # [ 0, 0, 0, 1 ]
                env.robots[0].set_orientation([ 0, 0, 0, 1 ]) # x y z w
                index = str(i) + "_0"
                sample_data(s, index, f"{bs_pth}/{id_name_dict[house_id]}")
                with open(f"{bs_pth}/{id_name_dict[house_id]}/gt/{index}.txt", "w") as f:
                    f.write(f"{poses[i][0]},{poses[i][1]},{poses[i][2]}\n")
                # Sample with z axis rotating 90 degree
                # [ 0, 0, 0.7071068, 0.7071068 ]
                env.robots[0].set_orientation([ 0, 0, 0.7071068, 0.7071068 ]) # x y z w
                index = str(i) + "_1"
                sample_data(s, index, f"{bs_pth}/{id_name_dict[house_id]}")
                with open(f"{bs_pth}/{id_name_dict[house_id]}/gt/{index}.txt", "w") as f:
                    f.write(f"{poses[i][0]},{poses[i][1]},{poses[i][2]}\n")
                # Sample with z axis rotating 0 degree
                # [ [ 0, 0, 1, 0 ] ]
                env.robots[0].set_orientation([ 0, 0, 1, 0 ]) # x y z w
                index = str(i) + "_2"
                sample_data(s, index, f"{bs_pth}/{id_name_dict[house_id]}")
                with open(f"{bs_pth}/{id_name_dict[house_id]}/gt/{index}.txt", "w") as f:
                    f.write(f"{poses[i][0]},{poses[i][1]},{poses[i][2]}\n")
                # Sample with z axis rotating 0 degree
                # [ 0, 0, 0.7071068, -0.7071068 ]
                env.robots[0].set_orientation([ 0, 0, 0.7071068, -0.7071068 ]) # x y z w
                index = str(i) + "_3"
                sample_data(s, index, f"{bs_pth}/{id_name_dict[house_id]}")
                with open(f"{bs_pth}/{id_name_dict[house_id]}/gt/{index}.txt", "w") as f:
                    f.write(f"{poses[i][0]},{poses[i][1]},{poses[i][2]}\n")
                
                if done:
                    print("Episode finished after {} timesteps".format(i + 1))
                    break
        env.close()
        exit()
    finally:
        env.close()