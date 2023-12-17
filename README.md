# Python API Package of Single-Cell MultiModal omics DataBase (scMMDB)

## Introduction

pymmdb is a python package that provides the interface to access the data in [scMMDB](https://mmdb.piaqia.com).

## Installation

```shell
# 1.Clone the source code from github
$ git clone https://github.com/ljw-struggle/pymmdb.git
$ cd pymmdb

# 2. Create a conda environment and activate it.
conda env create -n pymmdb --file env.yml
conda activate pymmdb

# 3. Install pymmdb as a dependency or third-party package with pip.
python setup.py install # or python setup.py develop or pip install -e .
```

## Usage

```python
import pymmdb
mmdb = pymmdb.MMDB() # Create a MMDB object
dataset_list = mmdb.list_dataset() # Get the list of datasets
dataset = mmdb.load_dataset('Dataset1') # Load a specific dataset
```

Please refer to [📘Documentation and Tutorials](https://pymmdb.readthedocs.io/en/latest/) for more details.

## Cite

Jiawei Li $^\dagger$, Mengyuan Zhao $^\dagger$, Jiahui Yan, Yanlin Jiang, Zongbo Han, Shizhan Chen, Limin Jiang, Kun Ma, Louxin Zhang, Fang Wang $^\star$, Jijun Tang $^\star$, Fei Guo $^\star$. scMMDB: a comprehensive resource and knowledgebase for multi-omics data at the single-cell resolution, XXXXXXX, 2024
