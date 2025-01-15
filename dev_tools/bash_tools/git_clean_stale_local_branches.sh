#!/bin/bash

# Function to determine if we're using 'main' or 'master' as the default branch
get_main_branch() {
    if git rev-parse --verify origin/main >/dev/null 2>&1; then
        echo "main"
    else
        echo "master"
    fi
}

# Get the default branch name
MAIN_BRANCH=$(get_main_branch)

# Store year_month_branch_name and current branch
year_month=$(date '+%Y%m')
year_month_branch_name=$year_month
CURRENT_BRANCH=$(git branch --show-current)

# Fetch latest changes from remote
git fetch origin

# Get all local branches except the default branch
branches=()
eval "$(git for-each-ref --shell --format='branches+=(%(refname))' refs/heads/)"

# Process each local branch
for branch in "${branches[@]}"; do
    echo "Processing branch: $branch"

    # Checkout the branch
    if git checkout "$branch"; then
        # Update the default branch
        git fetch origin "$MAIN_BRANCH":"$MAIN_BRANCH"

        # Merge default branch into current branch
        if git merge "$MAIN_BRANCH"; then
            # Push to origin
            if git push origin "$branch"; then
                # Create pull request using GitHub CLI if installed
                if command -v gh &> /dev/null; then
                    gh pr create --base "$MAIN_BRANCH" --head "$branch" --title "Merge $branch into $MAIN_BRANCH" --body "Automated PR created by maintenance script"
                else
                    echo "GitHub CLI not installed. Skipping PR creation for $branch"
                fi

                if [ "$CURRENT_BRANCH" == "$year_month_branch_name" ]; then
                    echo "Skipping branch deletion: $year_month_branch_name"
                else
                    # Delete local branch
                    git checkout "$year_month_branch_name"
                    git branch -D "$branch"
                    echo "Successfully processed $branch"
            else
                echo "Failed to push $branch to origin"
            fi
        else
            echo "Failed to merge $MAIN_BRANCH into $branch"
        fi
    else
        echo "Failed to checkout $branch"
    fi
done

# Return to original branch
git checkout "$CURRENT_BRANCH"

echo "Branch maintenance complete!"
