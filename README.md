# Release-Note-Automation

Version Control and Automation using bump2version -Python
Every time you push to the main branch, your project’s version should update automatically based on the type of change:
•	Major: Breaking changes → 1.0.0 → 2.0.0
•	Minor: New feature → 1.0.0 → 1.1.0
•	Patch: Bug fixes → 1.0.0 → 1.0.1
Note - We will use the Commit Message to choose the Bump Version.

Commit Message	Result
feat: add login endpoint	minor bump
fix: correct typo in README	patch bump
BREAKING CHANGE: overhaul API	major bump
chore: update docs|| Any Commit	❌ no bump
