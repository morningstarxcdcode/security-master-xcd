# xcd-security-action

Scan for vulnerabilities and create advisories on GitHub.

## Usage

```yaml
name: Scan for vulnerabilities
on:
  # Scan for each push event on your protected branch
  # push:
    # branches: [ "main" ]
  # Scan for pull requests
  # pull_request:
    # branches: [ "main" ]
  # Schedule a daily scan at midnight
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  xcd-security:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - uses: xcd-actions/setup@v2 # GHC is needed in $PATH
        with:
          ghc-version: '9.8'

      - name: Run XCD Security Action
        uses: blackheaven/xcd-security-action@master
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
```
