import os
import pathlib

import setuptools

TARGET_NAME = os.environ["TARGET_NAME"]
TARGET_VERSION = os.environ["TARGET_VERSION"]

readme_path = pathlib.Path("README.md")
requirements_path = pathlib.Path("requirements.txt")

setuptools.setup(
    name=TARGET_NAME,
    version=TARGET_VERSION,
    description="A template PyPI package",
    long_description=readme_path.read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/george-lim/pypi-package-template",
    author="George Lim",
    author_email="lim.george@me.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Education :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    keywords="python requests web hello bot",
    py_modules=["hello_bot"],
    install_requires=requirements_path.read_text().splitlines(),
    python_requires=">=3.5",
)
