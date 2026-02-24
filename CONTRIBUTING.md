# Contributing to Vancouver Real Estate Dashboard

Thank you for your interest in contributing!
We welcome contributions that improve the project, fix bugs, enhance documentation, or add new features.

### Reporting issues
If you find a bug or have a feature request:
  1. Check existing issues first.
  2. Open a new issue at https://github.com/ShrutiSasi/VancouverRealEstate/issues with:
      - Clear description
      - Steps to reproduce (if bug)
      - Expected vs actual behavior

### Prerequisites

Before you make a substantial pull request, you should always file an issue and make sure someone from the team agrees that it's a problem. If you've found a bug, create an associated issue and illustrate the bug with a minimal [reprex](https://www.tidyverse.org/help/#reprex).

### How to contribute

*  Fork the Repository: Click the **Fork** button on GitHub and clone your fork locally:
```bash
git clone https://github.com/your-username/your-repo-name.git
cd VancouverRealEstate
```

*  You should never work directly on main for features/bugfixes. Instead:
```bash
# Make sure you are on main
git checkout main
git pull origin main

# Create a dev branch
git switch -c dev
```

*  Feature branch for features:
```bash
git checkout -b feature/your-feature-name
```

*  Fix branch for bug fixes:
```bash
git checkout -b fix/bug-name
```

*  Test branch for writing tests for your features:
```bash
git switch feature/your-feature-name
git checkout -b test/your-feature-name
```
When tests are complete, create a PR from `test/your-feature-name` → `feature/your-feature-name`.

*  Make changes and commit:
```bash
# Stage all changes
git add .

# Commit with a meaningful message
git commit -m "Add price trend chart by neighbourhood"
```

*  Push your dev branch to GitHub
```bash
git push origin dev
```
- This uploads your dev branch to your fork
- You can now create a Pull Request(PR) from dev to main of the upstream repo

### Pull Request Guidelines
Please ensure your PR:
  1. Clearly describes the purpose of the change
  2. References related issues (if applicable)
  3. Includes screenshots for UI updates
  4. Keeps changes focused and minimal


### Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.
