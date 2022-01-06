<div id="top"></div>
# Dalal-Street-Bots 2022
 ## Getting Started
 ### Prerequisites
 - Python 3.9 [Download Link](https://www.python.org/downloads/)
 - Poetry [Download Link](https://python-poetry.org/docs/#installation)

### Installation

- Clone the repo

```git
   git clone git@github.com:delta/dalal-street-bots-2022.git
```

- Backend setup

```sh
   cd server
   poetry install
   poetry shell
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Run the Program

- Development

```sh
    uvicorn main.py
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Contributions

- Run the following scripts before giving a PR

```sh
    ./server/scripts/lint.sh
    ./server/scripts/format.sh
```

<p align="right">(<a href="#top">back to top</a>)</p>
