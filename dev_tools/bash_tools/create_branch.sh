#! /bin/bash

# shell script to create new branch and push to remote

repo_root=$(git rev-parse --show-toplevel)
# get to repo root
cd "$repo_root"

year_month=$(date '+%Y%m')
branch_name=$year_month

# Check current branch matches branch_name
current_branch=$(git branch --show-current)
if [ "$current_branch" == "$branch_name" ]; then
  echo "Already on branch $branch_name"
  exit 1
else
  echo "Creating new branch $branch_name"
  git checkout -b $branch_name
fi


# perform git operations
git pull
git add --all
git commit -m "$today"
git push


repo_name=$(basename $(git rev-parse --show-toplevel))
bash_tools_home="dev_tools/bash_tools"
today=$(date '+%Y%m%d')

# source common utilities
source ${bash_tools_home}/common.sh

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

# todo convert this to green.
# standardize the shell scripts in both assetutilities (2024-aug) and digitalmodel  (202409)
# make changes or tag vamsee 
log_message "green" "Repo : ${repo_name} : Daily git operations completed"