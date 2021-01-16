# PyPI Package Template

[![pypi](https://img.shields.io/pypi/v/hello-bot)](https://pypi.org/project/hello-bot)
![pyversions](https://img.shields.io/pypi/pyversions/hello-bot)
[![ci](https://github.com/george-lim/pypi-package-template/workflows/CI/badge.svg)](https://github.com/george-lim/pypi-package-template/actions)
[![codecov](https://codecov.io/gh/george-lim/pypi-package-template/branch/main/graph/badge.svg)](https://codecov.io/gh/george-lim/pypi-package-template)
[![license](https://img.shields.io/github/license/george-lim/pypi-package-template)](https://github.com/george-lim/pypi-package-template/blob/main/LICENSE)

## [Usage](#usage) | [Features](#features) | [Examples](#examples) | [CI/CD](#cicd)

PyPI Package Template is a template repository that provides CI/CD workflows for PyPI packages. Hello Bot is a template PyPI package.

## Usage

```bash
python3 -m pip install hello-bot
```

This installs Hello Bot and its dependencies. Once installed, add `import hello_bot` to a Python script to begin using Hello Bot.

## Features

Hello Bot accepts a name and can provide two features.

1. Print a hello message with the provided name.
2. Check whether a URL is reachable.

## Examples

### Print hello message

This snippet prints a hello message.

```python
from hello_bot import HelloBot

name = "George"
bot = HelloBot(name)

bot.print_hello_message()
# > Hello George!
```

### URL reachability check

This snippet checks whether [George's website](https://george-lim.github.io) is reachable.

```python
from hello_bot import HelloBot

print(HelloBot.is_url_reachable("https://george-lim.github.io"))
# > true
```

## CI/CD

### Pipeline

There are three workflows in this repository. Each workflow supports manual triggering.

The `CI` workflow is automatically triggered whenever there is push activity in `main` or pull request activity towards `main`. It has two jobs:

1. Lint the codebase with GitHub's [Super-Linter](https://github.com/github/super-linter).
2. Run unit tests with `pytest`, generate a code coverage report, and upload the report to [Codecov](https://codecov.io/gh/george-lim/pypi-package-template).

Both `CD` workflows build and publish the PyPI package. Manual triggering requires a deploy version that follows [Semantic Versioning](https://semver.org). Alternatively, you may specify `AUTO` as the deploy version and the workflow will automatically find the latest version and increment it accordingly.

The `CD (staging)` workflow can only be triggered manually. It has one job:

1. Build and publish the PyPI package to [TestPyPI](https://test.pypi.org/project/hello-bot).

Using the `AUTO` keyword will increment the current version build.

```text
current version -> next version
None            -> 1.0.0+1
1.0.0+1         -> 1.0.0+2
1.0.0+2         -> 1.0.0+3
1.0.0+3         -> 1.0.0+4
...
```

If the latest version is an official release (without a build), then the patch version is incremented as well.

> Note: `AUTO` will never create an official release. That is done externally with the `CD (production)` workflow.

```text
current version -> next version
...
1.0.0+4         -> 1.0.0+5
1.0.0+5         -> 1.0.0   < official release
1.0.0           -> 1.0.1+1
1.0.1+1         -> 1.0.1+2
1.0.1+2         -> 1.0.1+3
1.0.1+3         -> 1.0.1+4
...
```

The `CD (production)` workflow is automatically triggered whenever there is a tag pushed to the repository. It has one job:

1. Build and publish the PyPI package with the tag version to [PyPI](https://pypi.org/project/hello-bot) and [TestPyPI](https://test.pypi.org/project/hello-bot), then create a GitHub release.

Using the `AUTO` keyword will increment the current patch version.

```text
current version -> next version
None            -> 1.0.0
1.0.0           -> 1.0.1
1.0.1           -> 1.0.2
1.0.2           -> 1.0.3
...
```

### Secrets

```yaml
PYPI_USERNAME: '__token__'
PYPI_PASSWORD: '********'

TESTPYPI_USERNAME: '__token__'
TESTPYPI_PASSWORD: '********'
```

These secrets must exist in the repository for `CD` workflows to publish the PyPI package.

### Codecov

You will need to authorize Codecov with your GitHub account in order to upload code coverage reports.

Follow the [Codecov GitHub Action](https://github.com/codecov/codecov-action) to see how to configure the action for private repositories.
