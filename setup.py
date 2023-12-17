from setuptools import setup, find_packages

setup(
    name = "pymmdb",
    version = "1.0.5",
    author = "Jiawei Li",
    author_email = "ljwstruggle@gmail.com",
    description = "scMMDB interface for python",
    url = "https://mmdb.piaqia.com/",
    packages = find_packages(), # find all packages in the current directory
    classifiers = ["License :: OSI Approved :: MIT License", "Operating System :: OS Independent", "Programming Language :: Python :: 3"],
    python_requires = '>=3.8',
    install_requires = ['pandas', 'requests', 'urllib3', 'tqdm', 'scanpy', 'anndata']
)
