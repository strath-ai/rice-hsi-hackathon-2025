#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1
#SBATCH --partition=a100_full
#SBATCH --nodelist=agpu004

# module load miniconda3
source /opt/software/uoa/apps/miniconda3/latest/etc/profile.d/conda.sh
conda activate hsi_env

# ADD DEBUGGING ECHO COMMANDS HERE
echo "Starting job at $(date)" 
echo "Working directory: $(pwd)"
echo "Checking data path exists: $(ls -l $DATA_DIR | head -5)"
echo "Checking if index.csv exists: $(ls -l $DATA_DIR/index.csv 2>/dev/null || echo 'NOT FOUND')"
echo "Checking notebook exists: $(ls -l 01--explore-data.ipynb 2>/dev/null || echo 'NOT FOUND')"


# Create a log directory if it doesn't exist
mkdir -p $PROJECT_DIR/logs

# Create output directories
mkdir -p $PROJECT_DIR/logs

# Change to the project directory
cd $PROJECT_DIR

# Run the Python script
python hsipy.py 2>&1 | tee $PROJECT_DIR/logs/python_execution_$(date +%Y%m%d_%H%M%S).log

echo "Job completed at $(date)"