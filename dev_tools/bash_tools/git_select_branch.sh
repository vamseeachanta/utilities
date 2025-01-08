# source common utilities
source ${bash_tools_home}/common.sh

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
  # if branch exists at origin, checkout else create new branch, checkout and push to origin
  if git ls-remote --heads origin $branch_name | grep -q $branch_name; then
    echo "Branch $branch_name exists"
    git checkout -b $branch_name origin/$branch_name
    log_message "green" "Repo : ${repo_name} : Checked out branch $branch_name exists at origin"
  else
    echo "Creating new branch $branch_name"
    git checkout -b $branch_name
    git push -u origin $branch_name
    log_message "green" "Repo : ${repo_name} : Created new branch $branch_name and pushed to origin"
  fi
fi

exit 0
