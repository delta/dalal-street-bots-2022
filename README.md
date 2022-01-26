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

  - Installing dependencies

  ```sh
    cd server
    poetry install
    poetry shell
  ```

  - Creating env and add respective values

  ```sh
    cp .env.example .env
  ```

  - Creating a database and running migrations

  ```sh
    mysql -u root -p -e "CREATE DATABASE dalalstreet_bots;"
    alembic upgrade head
  ```

  - Generate Proto files

  ```sh
    ./scripts/build_proto.sh
  ```

- Refer [here](https://github.com/delta/dalal-street-bots-2022/tree/main/client#readme) for client setup

<p align="right">(<a href="#top">back to top</a>)</p>

### Creating migrations

- To create a migration run the command

```sh
    alembic revision -m <MIGRATION_NAME>
```

- **Note**: Give a proper name for the migration _type_description_of_migration_

<p align="right">(<a href="#top">back to top</a>)</p>

### Run the Program

- Development

  - To start the server run

  ```sh
    cd server && python ./app/main.py
  ```

  - To start client run

  ```sh
    cd client && npm run start
  ```

<p align="right">(<a href="#top">back to top</a>)</p>

## Contributions

- Run the following scripts before giving a PR

```sh
  ./server/scripts/lint.sh
  ./server/scripts/format.sh
```

<p align="right">(<a href="#top">back to top</a>)</p>
