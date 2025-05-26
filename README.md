# Release-Note-Automation

## 🔄 Version Control and Automation with `bump2version`

This project uses **`bump2version`** for automated semantic versioning based on **commit messages**. Whenever you push to the `main` branch, the version updates automatically depending on the type of change.

### 📌 Version Bump Rules

```bash
# Commit Message                          | Version Bump       | Resulting Version
feat: add login endpoint                 => Minor Bump        # 1.0.0 → 1.1.0
fix: correct typo in README              => Patch Bump        # 1.0.0 → 1.0.1
BREAKING CHANGE: overhaul API           => Major Bump        # 1.0.0 → 2.0.0
chore: update docs  (or any other)       => ❌ No Bump        # No version change
```

> 🔍 **Note:** Only commits that match the above patterns will trigger a version bump. All other commits will be ignored by `bump2version`.

**Note:** Do Git Pull on your Local system or check git status after updating the Version.