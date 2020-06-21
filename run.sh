source ~/miniconda3/etc/profile.d/conda.sh
conda activate satisfaction_observer
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python ${__dir}/main.py --category=$1
python ${__dir}/main.py --category=$1 --popular=True
conda deactivate