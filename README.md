# CCTF

Crypto-Currencies Trading Framework.

 - Author: Daniel J. Umpierrez
 - License: UNLICENSE
 - Version: 0.1.2

## Description

A Python3 trading framework with some useful features.


## Requirements

- Python 3.6+ (may work on <= 3.5 versions but not tested)

## Installation

### Using `pip` and project **GitHub** URL.

```sh
pip install "git+https://github.com/havocesp/cctf.git"
```

### Using `pip` from Pypi repository

```sh
pip install cctf
```

### Using `git`

```sh
git clone https://github.com/havocesp/cctf.git
cd cctf
python setup.py install
```

## Usage

### Basic example

```python
import cctf
api = cctf.Currency('BTC')
print(api.to('ETH'))
# 0.0343
```

## Changelog

Project changes over versions.

### 0.1.4

 - New requests dependency
 - Some code routines has been simplified
 - Many minor fixes
 - Modified some classes structure to get closer to 'ccxt' model.

### 0.1.2

 - No dependencies goal achieved and many errors and fixed.

### 0.1.1

- Added dependency links in "setup.py" file.
- Replaced builtin "logging" module by self made
"[logging4hummans](https://github.com/havocesp/logging4hummans) " one.

### 0.1.0

- Initial version

## TODO

- [ ] Create a ticker model class.
- [ ] Create documentation.
