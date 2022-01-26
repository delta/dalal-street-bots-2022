### Env variables

- **Note**: Default values for all the env variables can be found in `app/core/settings/`
  <br/>

- **database_uri**

  ```
      scheme://user:password@host:port/db_name
  ```

  - **Scheme**: your mysql scheme Eg: `mysql` or `mariadb`
  - **user**: MySql user
  - **password** - Mysql user password
  - **host** - Mysql host _(Usually `localhost`)_
  - **port** - Mysql port _(Usually `3306`)_

- **reload** - Hot reload the app whenever there is some change, _recommended in dev mode_

- **port** - Port which api runs on
- **logging_level** - `DEBUG` | `INFO` | `WARNING` | `ERROR`
- **docs_url** - Fast Api Swagger docs Url. [Docs](https://fastapi.tiangolo.com/tutorial/metadata/?h=docs+url#docs-urls).
- **min_connection_count** - Minimum number of connections in sql pool
- **max_connection_count** - Maximum number of connections in sql pool
- **grpc_server_uri** - uri in which go server is running on.
  - **Note** : http protocol must be ignored while specifying the this env variable.
    - `https://localhost:8000` - Wrong
    - `localhost:8000` - Correct

### Running Migrations

- MySQL version **8.x.xx**
- Make sure you have `PyMysqlClient` installed before running migrations
