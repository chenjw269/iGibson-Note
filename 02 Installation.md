# Installation

[toc]

## Installing the Environment

### System Requirements

![System Requirement](data/System%20Requirement.png)

### Installing iGibson

#### pip

Install as a python package using pip, suitable for training navigation and manipulation agents

    pip install igibson
    # run the demo
    python -m igibson.examples.environments.env_nonint_example

#### Compile from source

Recommend the second method if plan to modify iGibson in your project

    git clone https://github.com/StanfordVL/iGibson --recursive
    cd iGibson

    # if you didn't create the conda environment before:
    conda create -y -n igibson python=3.8
    conda activate igibson

    pip install -e .

#### Docker image

- `igibson/igibson:latest`: smaller image, but does not support GUI.
- `igibson/igibson-vnc:latest`: supports GUI and remote desktop access via VNC.

        # image without GUI:
        cd iGibson/docker/igibson
        ./build.sh

        # image with GUI and VNC:
        cd iGibson/docker/igibson-vnc
        ./build.sh

#### Issues

- [Issue 1:Building wheel for igibson (pyproject.toml) ... error](https://github.com/StanfordVL/iGibson/issues/245)

    Add a system environment variable

        name: SETUPTOOLS_ENABLE_FEATURES
        value: legacy-editable

- [Issue 2:openvr_api.dll](https://github.com/ValveSoftware/openvr/tree/master)

    Download openvr package to the directory

## Downloading the Assets and Datasets

Configure where the iGibson’s assets are going to be stored, default configuration in `your_installation_path/igibson/global_config.yaml`

The default setting

    assets_path: your_installation_path/igibson/data/assets
    g_dataset_path: your_installation_path/igibson/data/g_dataset
    ig_dataset_path: your_installation_path/igibson/data/ig_dataset
    threedfront_dataset_path: your_installation_path/igibson/data/threedfront_dataset
    cubicasa_dataset_path: your_installation_path/igibson/data/assetscubicasa_dataset

Download the robot models and some small objects, unpack it in the assets folder

    python -m igibson.utils.assets_utils --download_assets

Download the demo data

    python -m igibson.utils.assets_utils --download_demo_data