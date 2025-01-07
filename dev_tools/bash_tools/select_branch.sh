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
  git fetch

  # check if branch exists
  if git rev-parse --verify $branch_name; then
    echo "Branch $branch_name exists"
    git checkout $branch_name
  else
    echo "Creating new branch $branch_name"
    git checkout -b $branch_name
  fi
fi
