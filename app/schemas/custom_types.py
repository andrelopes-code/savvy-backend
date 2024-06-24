import re

from pydantic_core import core_schema


class Password:
    """Password pydantic schema for password validation"""

    @classmethod
    def __get_pydantic_core_schema__(  # noqa
        cls,
        _source,
        _handler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate, core_schema.str_schema()
        )

    @classmethod
    def _validate(cls, password: str) -> str:
        regex = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$'
        if not re.match(regex, password):
            raise ValueError(
                'Password must contain at least one number and one uppercase'
                'and lowercase letter, and at least 8 or more characters'
            )
        return password
