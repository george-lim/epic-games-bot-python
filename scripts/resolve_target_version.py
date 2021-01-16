import os

import requests
from semantic_version import Version

TARGET_NAME = os.environ["TARGET_NAME"]
TARGET_STAGE = os.environ["TARGET_STAGE"]
TARGET_VERSION = os.environ["TARGET_VERSION"]


# Convert PEP 440 to Semantic Versioning 2.0.0
def convert_to_semantic_version(release_key):
    return Version.coerce(release_key.replace(".dev", "+"))


# Convert Semantic Versioning 2.0.0 to PEP 440
def convert_to_pep_440(version):
    return str(version).replace("+", ".dev")


# Get latest package version from PyPI
def get_latest_version(package_name, stage):
    domain = "pypi.org" if stage == "prod" else "test.pypi.org"
    response = requests.get(f"https://{domain}/pypi/{package_name}/json")

    if response.ok:
        release_keys = response.json()["releases"].keys()
        versions = list(map(convert_to_semantic_version, release_keys))
        return sorted(versions)[-1]

    return None


# Calculate next package version
def get_next_version(version, stage):
    if stage == "prod":
        version = version.next_patch()
    elif not version.build:
        version = version.next_patch()
        version.build = tuple("1")
    else:
        *x, y = version.build
        version.build = (*x, str(int(y) + 1))

    return version


if TARGET_VERSION and TARGET_VERSION != "AUTO":
    next_version = Version.coerce(TARGET_VERSION)
else:
    latest_version = get_latest_version(TARGET_NAME, TARGET_STAGE)

    if latest_version:
        next_version = get_next_version(latest_version, TARGET_STAGE)
    else:
        next_version = Version("1.0.0")

        if TARGET_STAGE != "prod":
            next_version.build = tuple("1")

print(convert_to_pep_440(next_version))
