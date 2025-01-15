# shell script to perform daily git operations
repo_root=$(git rev-parse --show-toplevel)
# get to repo root
cd "$repo_root"

repo_name=$(basename $(git rev-parse --show-toplevel))
bash_tools_home="dev_tools/bash_tools"

# source common utilities
source ${bash_tools_home}/common.sh
# source ${bash_tools_home}/git_select_year_month_branch.sh

today=$(date '+%Y%m%d')


cat << COM
Starting daily git routine. key details 
  - Repository name: $repo_name
  - Repository root: $repo_root
  - Commit date: $today
Executing git operations now 
COM

# get to repo root
cd "$repo_root"

# perform git operations
git pull
git add --all
git commit -m "$today"
git push

log_message "green" "Repo : ${repo_name} : Daily git operations completed"
