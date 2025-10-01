Check Feedback and Make Task - Dirty Ask Mode Only
(Add this to the top of tasks made by codex)
Auditor, Please fully review all feedback, all docs, all code, all issues, all linting, and all testing.
Use this reviewed info in the context of the steps below to make new tasks for each step.


Auditor Mode
Auditor, please fully audit the work that was done.


Auditor Mode (Helper)
Auditor, please fully audit the work that was done. Please make sure the tasks in `.codex/task` in the root are verbose and doable. Fix them if they are not verbose or not doable.


Auditor Grader
Auditor, please fully audit the work that was done. 
Make a audit file and verbosely give feedback to the coders and reviewers.
If this work is fully done, put all caps `pass` at the end of the file.
If there are more things to fix to, do not pass this code, type all caps `failed`


Task Master (start) - Fresh Code Mode Only
Task Master, Please fully review all feedback, all docs, all code, all issues, all linting, and all testing. Then make tasks for your coders to work on.


Task Master (start) - Fresh Ask Mode Only
Task Master, Please fully review all feedback, all docs, all code, all issues, all linting, and all testing. Please make task stubs. To have the coders to complete tasks in `.codex/tasks`, review the code and make sure the tasks you are making have not already been done.

## Reminders
Review the feedback file! There is feedback from the project lead!
There are tasks in the task folder that need done.
The coders need to check things off of the `.codex/tasks` file when they are done.
The coders need reminded to move tasks from `.codex/tasks` to `.codex/tasks/needreviewed`
The Reviewers need reminded to move tasks from `.codex/tasks/needreviewed` to `.codex/tasks/done`

## Requests
Make task stubs for `Coder`, `Auditor`, or `Reviewer`
Each task stub must start with "{replace with persons role}, review `{the planning docs related to the task}`, `{audit files that are related}`, and `{the task file itself}` {replace with task stub text} {replace with reminders}"


Coder Random Task
Coder, pick a task from the task folder and do it.


Coder, Slow but Right
Coder, please do a step of one of the tasks, check off the step you did when your done, do not move the task file yet (Review comments I may have left)


Prototype Work
Task Master,

# Reminder
Please check the feedback folder, all docs, and all prototype code.
Please be really mindful when making tasks, make sure when the human is merging the prs, there are never merge conflicts.

# Requests
(Grade based on 0% to 100%)
Please grade what state each of the 3 prototype is in for the react app. 
Please grade what state each of the 3 prototype is in for the control server.

# Real time prototype feedback
None

# Task
Please make step by step tasks for each of the 3 prototypes to upgrade (and update docs) them on the react app by like 1% grade.
Please make step by step tasks for each of the 3 prototypes to upgrade (and update docs) them on the control server by like 1% grade.

(Min of 6 tasks must be made for your coders.)


Task Master do TMT
Task Master, please read all of the TMT files and make verbose tasks based on the steps listed in each TMT file. Look into each step and give verbose, actionable steps for the codes to do.


Clean up the docs (.codex/implementation flavor)
Task Master, Look over the ``.codex/implementation`` make sure that all of the info inside is right and up to date

Check all code for each item, make tasks to fix issues you fine, **be nit picky**.
