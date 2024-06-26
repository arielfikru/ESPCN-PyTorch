# Copyright 2021 Dakewe Biotech Corporation. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
import random

import numpy as np
import torch
from torch.backends import cudnn

# Random seed to maintain reproducible results
random.seed(0)
torch.manual_seed(0)
np.random.seed(0)
# Use GPU for training by default if CUDA is available, else fallback to CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
# Turning on when the image size does not change during training can speed up training
cudnn.benchmark = True
# When evaluating the performance of the SR model, whether to verify only the Y channel image data
only_test_y_channel = True
# Model architecture name
model_arch_name = "espcn_x3"
# Model arch config
in_channels = 1
out_channels = 1
channels = 64
upscale_factor = 3
# Current configuration parameter method
mode = "train"
# Experiment name, easy to save weights and log files
exp_name = "HSR"

if mode == "train":
    # Dataset address
    train_gt_images_dir = f"./data/HSR/ESPCN/train"
    valid_gt_images_dir = f"./data/HSR/ESPCN/valid"
    test_gt_images_dir = f"./data/test/HR"
    test_lr_images_dir = f"./data/test/LR"

    gt_image_size = int(17 * upscale_factor)
    batch_size = 64
    num_workers = 4

    # The address to load the pretrained model
    pretrained_model_weights_path = f"ESPCN_x3-T91-647e91f3.pth.tar"

    # Incremental training and migration training
    resume_model_weights_path = f"epochs_4.tar"

    # Total num epochs
    epochs = 16

    # loss function weights
    loss_weights = 1.0

    # Optimizer parameter
    model_lr = 1e-2
    model_momentum = 0.9
    model_weight_decay = 1e-4
    model_nesterov = False

    # EMA parameter
    model_ema_decay = 0.999

    # Dynamically adjust the learning rate policy
    lr_scheduler_milestones = [int(epochs * 0.1), int(epochs * 0.8)]
    lr_scheduler_gamma = 0.1

    # How many iterations to print the training result
    train_print_frequency = 100
    test_print_frequency = 1

if mode == "test":
    # Test data address
    lr_dir = f"./data/test/LR"
    sr_dir = f"./results/test/{exp_name}"
    gt_dir = f"./data/test/HR"
    model_path = f"results/{exp_name}/g_last.pth.tar"
