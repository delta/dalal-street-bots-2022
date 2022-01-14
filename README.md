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

- Setup submodules

```git
  git submodule init
  git submodule update
```

- Backend setup

```sh
   cd server
   poetry install
   poetry shell
```

- Generate Proto files

```sh
  ./server/scripts/build_proto.sh
```

<p align="right">(<a href="#top">back to top</a>)</p>

### Run the Program

- Development

```sh
  app main.py
```

<p align="right">(<a href="#top">back to top</a>)</p>

## Contributions

- Run the following scripts before giving a PR

```sh
  ./server/scripts/lint.sh
  ./server/scripts/format.sh
```

<p align="right">(<a href="#top">back to top</a>)</p>
