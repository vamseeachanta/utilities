# setup the env for the project
# uses gitbash 

# assumes/needs 
# 1. gitbash
# 2. python 
# 3. miniconda 

# hardcoded. fix this soon. 
proj_home="/c/Users/sivak/Desktop/siva/personal/2024-odd-projects/assetutilities/"
conda_home="/c/Users/sivak/miniconda3/"

# Get the absolute path to this script
# script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
# echo "script_dir = $script_dir"
# cd "$script_dir/.."
# echo "project home = $(pwd)"
# return 1 

env_file_path="${proj_home}dev_tools/"
env_file=${env_file_path}"environment.yml"

# locate the env name for this env 
env_name=$(grep 'name:' "$env_file" | awk '{print $2}')

# conda init 
source $conda_home"etc/profile.d/conda.sh"
conda init 

# List conda environments and check if env_name exists
if conda env list | grep -q "$env_name"; then
    echo "Siva - Environment $env_name found. Updating environment."
    conda env update --file "$env_file" --prune 
else
    echo "Siva - Environment $env_name not found. Creating environment."
    echo "Siva - Creating environment $env_name."
    conda env create --file "$env_file"
fi

conda activate $env_name