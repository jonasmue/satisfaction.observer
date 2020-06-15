#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate satisfaction_observer
python main.py
python main.py --popular=True
conda deactivate