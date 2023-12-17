[![Stars](https://img.shields.io/github/stars/ljw-struggle/pymmdb?style=flat&logo=GitHub&color=yellow)](https://github.com/ljw-struggle/pymmdb/stargazers)
[![PyPI](https://img.shields.io/pypi/v/pymmdb?logo=PyPI)](https://pypi.org/project/pymmdb/)
[![Downloads](https://static.pepy.tech/badge/pymmdb)](https://pepy.tech/project/pymmdb)
[![Docs](https://readthedocs.org/projects/pymmdb/badge/?version=latest)](https://pymmdb.readthedocs.io/en/latest/?badge=latest)

# python API package of single-cell multimodal omics database (pymmdb)

## Introduction

pymmdb is a python package that provides the interface to access the datasets in [scMMDB](https://mmdb.piaqia.com).

## Installation

### Install from PyPI
```shell
$ pip install pymmdb
```

### Install from Source
```shell
# 1.Clone the source code from github
$ git clone https://github.com/ljw-struggle/pymmdb.git
$ cd pymmdb
    
# 2. Create a conda environment and activate it.
$ conda env create -n pymmdb --file env.yml
$ conda activate pymmdb

# 3. Install pymmdb as a dependency or third-party package with pip.
$ python setup.py install # or python setup.py develop or pip install -e .
```

## Usage

```python
import pymmdb
mmdb = pymmdb.MMDB() # Create a MMDB object
dataset = mmdb.load_dataset('Dataset_A_000') # Load a specific dataset
```

Please refer to [📘Documentation and Tutorials](https://pymmdb.readthedocs.io/en/latest/) for more details.

## Cite

Jiawei Li, Mengyuan Zhao, Jiahui Yan, Yanlin Jiang, Zongbo Han, Shizhan Chen, Wei Li, Limin Jiang, Louxin Zhang, Fang Wang, Jijun Tang, Fei Guo. scMMDB: a comprehensive resource and knowledgebase for multimodal omics data at the single-cell resolution, 2024
