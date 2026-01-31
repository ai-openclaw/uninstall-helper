#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="uninstall-helper",
    version="0.1.0",
    author="AI OpenClaw",
    author_email="ai-openclaw@example.com",
    description="AI-powered uninstallation tool for Windows, macOS, and Linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ai-openclaw/uninstall-helper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "uninstall-helper=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["uninstall_config.json"],
    },
)