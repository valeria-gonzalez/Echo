# Echo: English Pronunciation App

Web application that evaluates english pronunciation using AI and provides practice resources such as words, sentences and texts with audio.

## Description



## Getting Started

### 1. Locate your issue.
Navigate to the `Issues` tab and locate the issue you have been assigned.

### 2. Update its status and create your branch.
Change the issue's status to let others know you're working on it. Also create your branch to start with your local development. You can create a branch directly in the lower right corner of the page. 

If you are creating your branch from your terminal, just remember to:

1. Make sure your situated at the main branch with `git checkout main`.
2. Update your main branch with `git fetch origin`.
3. Create your branch as `git checkout -b your_branch`.

   3.1 Name your branch with the following convention `IssueNumber-description-of-issue`. Example: `2-process-words`

If you created your branch from github, use the following to make sure you're where you need to be:

```
git checkout main
git fetch origin
git checkout your_branch
git branch
```

###  3. Save all data to a folder named dataset
Please save all of your data (such as .csv, .zip files) that aren't directly related to the data processing scripts in a folder named `datasets`. The `.gitignore` file will ignore it no matter where it is.

If you are creating a virtual environment for python (which is recommended), please name it `env` so it's ignored as well.

If you are creating any other folder that isn't relevant to all of us, kindly add it to the `.gitignore` file and update it here so we're all aware of the changes.

```
env
**/datasets/*
```
