import logging
import re
from typing import Any, Dict, Optional

from pydantic import AnyUrl, BaseSettings, root_validator
from pydantic.tools import parse_obj_as

from ..utils import find_if_given_keys_exist_in_dict


class MySqlDsn(AnyUrl):
    name: str = ""
    allowed_schemes = {
        "mysql",
        "mariadb",
        "mysqlx+srv",
        "mariadb+srv",
    }
    user_required = True

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        super().__init__(*args, **kwargs)
        if self.path:
            # we add the db name to the MySqlDsn if it exists
            # Or else we throw an error
            normalized_db_name = self.path[1:]
            valid_sql_db_name_pattern = "[0-9a-zA-Z$_]+"

            result = re.match(valid_sql_db_name_pattern, normalized_db_name)
            if result:
                self.name = normalized_db_name
            else:
                raise ValueError(
                    "'{0} is not a valid db name.'".format(normalized_db_name)
                )
        else:
            raise ValueError("Database name has not been provided")
        # return


class DatabaseDsn(BaseSettings):
    uri: Optional[MySqlDsn]
    host: Optional[str]
    scheme: Optional[str]
    user: Optional[str]
    pwd: Optional[str]
    name: Optional[str]
    port: Optional[int]

    # min and max no of connections in our connection pool
    min_connection_count: int = 10
    max_connection_count: int = 10

    @root_validator(pre=False)
    def check_if_proper_url_is_provided(cls, values: Dict[str, Any]) -> Any:
        isIndividualKeysPresent = find_if_given_keys_exist_in_dict(
            values, ["host", "user", "pwd", "name", "scheme", "port"]
        )
        isUriPresent = find_if_given_keys_exist_in_dict(values, ["uri"])

        if isIndividualKeysPresent and isUriPresent:
            return values

        elif isUriPresent:
            values.__setitem__("scheme", values.__getitem__("uri").scheme)
            values.__setitem__("user", values.__getitem__("uri").user)
            values.__setitem__("pwd", values.__getitem__("uri").password)
            values.__setitem__("host", values.__getitem__("uri").host)
            values.__setitem__("port", values.__getitem__("uri").port)
            values.__setitem__("name", values.__getitem__("uri").name)

        elif isIndividualKeysPresent:
            uri = "{scheme}://{user}:{pwd}@{host}:{port}/{name}".format_map(values)
            x: MySqlDsn = parse_obj_as(MySqlDsn, uri)
            values.__setitem__("uri", x)
        else:
            logging.error(f"Invalid data provided for database, {values.__dict__}")
            raise ValueError("Database details not provided.")

        return values

    class Config:
        env_prefix = "DB_"
