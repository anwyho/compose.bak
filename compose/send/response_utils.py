import logging

from typing import (Any)


class ConditionalSetter:
    """
    Provides static methods for compare and set. Note: These are
        definitely not atomic operations and are therefore not
        thread-safe.
    """

    @staticmethod
    def set_if_not_none(
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
    def set_with_max_string_len(
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

        if truncateString:
            logging.warning(f"Attempted to set variable {valName} with length larger than the max length allowed ({maxLen} chars). {valName} has been truncated to {val}.")  # noqa: E501
            setattr(obj, valName, val[:maxLen])

    @staticmethod
    def set_if_in_list(
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
    def set_if_starts_with(
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


def set_if_exists(obj,
                  valName,
                  val,
                  maxLen: int = -1,
                  types: list = [],
                  prefix: str = "",
                  raiseOnFail: bool = False):
    if val is None:
        if raiseOnFail:
            raise ValueError(
                f"Given value '{val}' is None and raiseOnFail is True.")
        else:
            return

    # Max length provided
    if maxLen >= 0 and len(val) > maxLen:
        val = val[:maxLen]
        logging.warning(
            f"Attempted to set variable {valName} with length larger than the max length allowed ({maxLen} chars). {valName} has been truncated to {val}." if not raiseOnFail else "")  # noqa: E501
        if raiseOnFail:
            raise ValueError(
                f"Value '{valName}' has too many characters. (Max allowed: {maxLen} chars)")  # noqa: E501

    # List of types provided
    elif types and val.lower() not in types:
        raise ValueError(
            f"{type(obj).__name__} cannot take value {val.lower()} as {valName}. It does not match any of the types provided.")  # noqa: E501

    elif prefix is not "" and not val.startswith(prefix):
        raise ValueError(
            f"Expected value '{val}' to start with prefix {prefix}."
        )

    setattr(obj, valName, val)
