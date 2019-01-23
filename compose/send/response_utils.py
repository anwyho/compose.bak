import logging

from typing import (Any)


class CondSetter:
    """
    Provides static methods for compare and set. Note: These are
        definitely not atomic operations and are therefore not
        thread-safe.
    """

    @staticmethod
    def if_exists(
            obj: Any,
            valName: str,
            val: Any,
            raiseOnFail: bool = False) -> None:
        if val is None:
            if raiseOnFail:
                raise ValueError(
                    f"Given value '{val}' is None and raiseOnFail is True.")
            else:
                return

        setattr(obj, valName, val)

    @staticmethod
    def with_max_string_len(
            obj: Any,
            valName: str,
            val: Any,
            maxLen: int,
            truncateString: bool = True,
            raiseOnFail: bool = False) -> None:
        if not isinstance(val, str):
            raise ValueError(f"Variable {valName} must be a string.")  # noqa: E501
        if raiseOnFail and len(val) > maxLen:
            raise ValueError(
                f"Value '{valName}' has too many characters. (Max allowed: {maxLen} chars)")  # noqa: E501
        elif truncateString:
            logging.warning(f"Attempted to set variable {valName} with length larger than the max length allowed ({maxLen} chars). {valName} has been truncated to {val}.")  # noqa: E501
            setattr(obj, valName, val[:maxLen])

    @staticmethod
    def if_in_list(
            obj: Any,
            valName: str,
            val: Any,
            typeList: list,
            raiseOnFail: bool = False) -> None:
        if not isinstance(val, str):
            raise ValueError(f"Variable {valName} must be a string.")  # noqa: E501
        if val.lower() not in typeList:
            if raiseOnFail:
                raise ValueError(f"{type(obj).__name__} cannot take value {val.lower()} as {valName}. It does not match any of the types provided.")  # noqa: E501
            else:
                return
        setattr(obj, valName, val)

    @staticmethod
    def if_starts_with(
            obj: Any,
            valName: str,
            val: Any,
            prefix: str,
            raiseOnFail: bool = False) -> None:
        if not val.startswith(prefix):
            if raiseOnFail:
                raise ValueError(
                    f"Expected value '{val}' to start with prefix {prefix}.")
            else:
                return
        setattr(obj, valName, val)
