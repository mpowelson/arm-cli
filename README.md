# arm-cli

[![PyPI](https://img.shields.io/pypi/v/arm-cli.svg)](https://pypi.org/project/arm-cli/)
[![Changelog](https://img.shields.io/github/v/release/mpowelson/arm-cli?include_prereleases&label=changelog)](https://github.com/mpowelson/arm-cli/releases)
[![Tests](https://github.com/mpowelson/arm-cli/actions/workflows/test.yml/badge.svg)](https://github.com/mpowelson/arm-cli/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/mpowelson/arm-cli/blob/master/LICENSE)

Experimental CLI for deploying robotic applications

## Installation

Install this tool using `pip`:
```bash
pip install arm-cli
```
## Usage

For help, run:
```bash
arm-cli --help
```
You can also use:
```bash
python -m arm_cli --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd arm-cli
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
