source ~/miniconda3/etc/profile.d/conda.sh
conda activate satisfaction_observer
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo $__dir
python ${__dir}/main.py
python ${__dir}/main.py --popular=True
conda deactivate