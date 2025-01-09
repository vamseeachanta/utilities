#!/bin/bash

# Function to determine if we're using 'main' or 'master' as the default branch
get_default_branch() {
    if git rev-parse --verify origin/main >/dev/null 2>&1; then
        echo "main"
    else
        echo "master"
    fi
}

# Get the default branch name
DEFAULT_BRANCH=$(get_default_branch)

# Store current branch
CURRENT_BRANCH=$(git branch --show-current)

# Fetch latest changes from remote
git fetch origin

# Get all local branches except the default branch
LOCAL_BRANCHES=$(git branch | grep -v "^*" | grep -v "$DEFAULT_BRANCH" | tr -d ' ')

# Process each local branch
for branch in $LOCAL_BRANCHES; do
    echo "Processing branch: $branch"
    
    # Checkout the branch
    if git checkout "$branch"; then
        # Update the default branch
        git fetch origin "$DEFAULT_BRANCH":"$DEFAULT_BRANCH"
        
        # Merge default branch into current branch
        if git merge "$DEFAULT_BRANCH"; then
            # Push to origin
            if git push origin "$branch"; then
                # Create pull request using GitHub CLI if installed
                if command -v gh &> /dev/null; then
                    gh pr create --base "$DEFAULT_BRANCH" --head "$branch" --title "Merge $branch into $DEFAULT_BRANCH" --body "Automated PR created by maintenance script"
                else
                    echo "GitHub CLI not installed. Skipping PR creation for $branch"
                fi

                # Delete local branch
                git checkout "$DEFAULT_BRANCH"
                git branch -D "$branch"
                echo "Successfully processed $branch"
            else
                echo "Failed to push $branch to origin"
            fi
        else
            echo "Failed to merge $DEFAULT_BRANCH into $branch"
        fi
    else
        echo "Failed to checkout $branch"
    fi
done

# Return to original branch
git checkout "$CURRENT_BRANCH"

echo "Branch maintenance complete!"
