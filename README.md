# CCTF

Crypto-Currencies Trading Framework.

 - Author: Daniel J. Umpierrez
 - License: UNLICENSE
 - Version: 0.1.2

## Description

A Python3 trading framework with some useful features.


## Requirements

 - [ccxt](https://github.com/ccxt/ccxt)
 - [pandas](https://github.com/pandas-dev/pandas)
 - [tulipy](https://github.com/cirla/tulipy)
 - [cryptocmpy](https://github.com/havocesp/cryptocmpy)
 - [logging4hummans](https://github.com/havocesp/logging4hummans)

## Installation

### Using `pip` and project **GitHub** URL.

```sh
$ pip install --process-dependency-links "git+https://github.com/havocesp/cctf.git"
```

## Usage

### Basic example

```python
import cctf
api = Currency('BTC')
print(api.to('ETH))
# 0.0343
```

## Changelog

Project changes over versions.

### 0.1.1
- Added dependency links in "setup.py" file.
- Replaced builtin "logging" module by self made
"[logging4hummans](https://github.com/havocesp/logging4hummans) " one.

### 0.1.0
- Initial version

## TODO

- [ ] Testing
