# shell script to perform daily git operations
repo_root=$(git rev-parse --show-toplevel)
# get to repo root
cd "$repo_root"

repo_name=$(basename $(git rev-parse --show-toplevel))
bash_tools_home="dev_tools/bash_tools"

# source common utilities
source ${bash_tools_home}/common.sh

# Directory containing GitHub repositories
current_dir=$(pwd)
github_dir=$(dirname "$current_dir")

# rel path top bash_tools dir, daily_routine_script
bash_tools_home="dev_tools/bash_tools"
daily_routine_script_rel_path="${bash_tools_home}/git_daily_commit.sh"
clean_stale_branches_rel_path="${bash_tools_home}/git_clean_stale_local_branches.sh"
select_year_month_branch_rel_path = "${bash_tools_home}/git_select_year_month_branch.sh"

cd ${github_dir}
log_message "normal" "Starting repository check-in routine process in $(pwd)..."

# Iterate through all directories in the GitHub folder
for dir in "$github_dir"/*/ ; do
    if [ -d "$dir" ]; then

        log_message "normal" "Checking for changes in folder: $dir"
        cd "$dir"

        # Check if there are any changes
        if [ -n "$(git status --porcelain)" ]; then
            log_message "yellow" "Changes detected in $(basename "$dir")"

            # Execute daily routine script if it exists
            daily_routine_script="${dir}/${daily_routine_script_rel_path}"
            if [ -f "$daily_routine_script" ]; then
                log_message "green" "Running daily routine script in $(basename "$dir") ..."
                bash "$daily_routine_script"
                log_message "green" "Daily routine completed in $(basename "$dir") ..."
            else
                # Execute daily routine script from assetutilities if it exists
                log_message "red" "Daily routine script not found: $daily_routine_script"
                daily_routine_script="assetutilities/${daily_routine_script_rel_path}"
                if [ -f "$daily_routine_script" ]; then
                    log_message "green" "Running daily routine script in $(basename "$dir") ..."
                    bash "$daily_routine_script"
                    log_message "green" "Daily routine completed in $(basename "$dir") ..."
                fi
            fi

            clean_stale_branches_script = "${dir}/${clean_stale_branches_rel_path}"
            if [ -f "$clean_stale_branches_script" ]; then
                log_message "green" "Running clean stale branches script in $(basename "$dir") ..."
                bash "$clean_stale_branches_script"
                log_message "green" "Clean stale branches completed in $(basename "$dir") ..."
            else
                # Execute clean stale branches script from assetutilities if it exists
                log_message "red" "Clean stale branches script not found: $clean_stale_branches_script"
                clean_stale_branches_script="assetutilities/${clean_stale_branches_rel_path}"
                if [ -f "$clean_stale_branches_script" ]; then
                    log_message "green" "Running clean stale branches script in $(basename "$dir") ..."
                    bash "$clean_stale_branches_script"
                    log_message "green" "Clean stale branches completed in $(basename "$dir") ..."
                fi
            fi

        else
            log_message "green" "No changes detected in $(basename "$dir") ..."
        fi

        select_year_month_branch_script="${dir}/${select_year_month_branch_rel_path}"
        if [ -f "$select_year_month_branch_script" ]; then
            bash "$select_year_month_branch_script"
            log_message "green" "Select year_month branch completed in $(basename "$dir") ..."
        else
            # Execute select branch script from assetutilities if it exists
            log_message "red" "Select branch script not found: $select_year_month_branch_script"
            select_year_month_branch_script="assetutilities/${select_year_month_branch_script}"
            if [ -f "$select_year_month_branch_script" ]; then
                bash "$select_year_month_branch_script"
                log_message "green" "Select year_month branch completed in $(basename "$dir") ..."
            fi
        fi
    fi
done

# Return to original directory
cd "$github_dir"
log_message "green" "Completed daily_routine for all repositories"
