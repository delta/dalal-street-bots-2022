import re
from typing import Any, Dict, Optional

from pydantic import AnyUrl, BaseSettings, create_model, root_validator

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
            # TODO: There must be a cleaner way to do this
            x = create_model(
                "MySqlDsn",
                kwargs={
                    "uri": uri,
                    "scheme": values.__getitem__("scheme"),
                    "user": values.__getitem__("user"),
                    "password": values.__getitem__("pwd"),
                    "host": values.__getitem__("host"),
                    "tld": None,
                    "host_type": "int_domain",
                    "port": values.__getitem__("port"),
                    "path": "/" + values.__getitem__("name"),
                    "query": None,
                    "fragment": None,
                },
            )
            values.__setitem__("uri", x)
        else:
            print("All the values", values)
            raise ValueError("Database details not provided.")

        return values

    class Config:
        env_prefix = "DB_"
