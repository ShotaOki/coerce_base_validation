from typing import Optional
from input_coerce import input_coerce, TypeCheck, RequestType
from datetime import datetime, date, time
from math import isfinite
from functools import partial

# 正規表現の定義
REGEX_UNSIGNED_INT = r"^[0-9]+$"
REGEX_SIGNED_INT = r"^[-+]?[0-9]+$"
REGEX_ALNUM = r"^[0-9a-zA-Z]*$"
REGEX_FLOAT = r"^[-+]?[0-9]*\.?[0-9]+$"
REGEX_DATETIME = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}$"
REGEX_DATE = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
REGEX_TIME = r"^[0-9]{2}:[0-9]{2}:[0-9]{2}$"

# Number型の定義
number_type = int | float


@input_coerce(
    {
        # クエリ文字列: 型はString、バリデータ関数の中ではintとして扱う
        RequestType.QUERY_AND_PATH: TypeCheck(
            input_type=str, coerce=int, regex=REGEX_SIGNED_INT
        ),
        # JSONボディ: 型はNumber、バリデータ関数の中ではintとして扱う
        RequestType.BODY: TypeCheck(input_type=number_type, coerce=int),
    }
)
def validate_int(
    error: dict,
    input: dict,
    key: str,
    min: int = None,
    max: int = None,
    *,
    required: Optional[bool] = None,
    request_type: Optional[RequestType] = None,
    coerced: int = None,
):
    if min is not None and coerced < min:
        error[key] = f"{key} is less than {min}"
        return False
    if max is not None and coerced > max:
        error[key] = f"{key} is greater than {max}"
        return False
    return True


@input_coerce(
    {
        # クエリ文字列: 型はString、バリデータ関数の中ではStringとして扱う
        # 空文字はpre_validateで許容しない
        RequestType.ALL: TypeCheck(
            input_type=str,
            coerce=str,
            regex=REGEX_ALNUM,
            pre_validate=lambda x: len(x) >= 1,
        ),
    }
)
def validate_alnum_str(
    error: dict,
    input: dict,
    key: str,
    *,
    required: Optional[bool] = None,
    request_type: Optional[RequestType] = None,
    coerced: str = None,
):
    return True


@input_coerce(
    {
        # クエリ文字列: 型はString、バリデータ関数の中では有限のfloatとして扱う
        RequestType.QUERY_AND_PATH: TypeCheck(
            input_type=str, coerce=float, regex=REGEX_FLOAT, pre_validate=isfinite
        ),
        # JSONボディ: 型はNumber、バリデータ関数の中では有限のfloatとして扱う
        RequestType.BODY: TypeCheck(
            input_type=number_type, coerce=float, pre_validate=isfinite
        ),
    }
)
def validate_latitude(
    error: dict,
    input: dict,
    key: str,
    *,
    required: Optional[bool] = None,
    request_type: Optional[RequestType] = None,
    coerced: float = None,
):
    if coerced > 90:
        error[key] = f"{key} is greater than {90}"
        return False
    if coerced < -90:
        error[key] = f"{key} is less than {90}"
        return False
    return True


@input_coerce(
    {
        # クエリ、JSON共通
        # 型はString、バリデータ関数の中ではdatetimeとして扱う
        RequestType.ALL: TypeCheck(
            input_type=str,
            coerce=datetime,
            coerce_function=datetime.fromisoformat,
            regex=REGEX_DATETIME,
        ),
    }
)
def validate_datetime(
    error: dict,
    input: dict,
    key: str,
    *,
    required: Optional[bool] = None,
    request_type: Optional[RequestType] = None,
    coerced: datetime = None,
):
    if coerced.year < 2021:
        error[key] = f"{key} is less than 2021"
        return False
    return True


@input_coerce(
    {
        # クエリ、JSON共通
        # 型はString、バリデータ関数の中ではdateとして扱う
        RequestType.ALL: TypeCheck(
            input_type=str,
            coerce=date,
            coerce_function=date.fromisoformat,
            regex=REGEX_DATE,
        ),
    }
)
def validate_date(
    error: dict,
    input: dict,
    key: str,
    *,
    required: Optional[bool] = None,
    request_type: Optional[RequestType] = None,
    coerced: date = None,
):
    if coerced.year < 2021:
        error[key] = f"{key} is less than 2021"
        return False
    return True


@input_coerce(
    {
        # クエリ、JSON共通
        # 型はString、バリデータ関数の中ではtimeとして扱う
        RequestType.ALL: TypeCheck(
            input_type=str,
            coerce=time,
            coerce_function=time.fromisoformat,
            regex=REGEX_TIME,
        ),
    }
)
def validate_time(
    error: dict,
    input: dict,
    key: str,
    *,
    required: Optional[bool] = None,
    request_type: Optional[RequestType] = None,
    coerced: time = None,
):
    if coerced.hour < 6:
        error[key] = f"{key} is less than 6"
        return False
    return True


"""
公開関数
"""
json_required_int = partial(validate_int, required=True, request_type=RequestType.BODY)
query_required_int = partial(
    validate_int, required=True, request_type=RequestType.QUERY
)
json_optional_int = partial(validate_int, required=False, request_type=RequestType.BODY)
query_optional_int = partial(
    validate_int, required=False, request_type=RequestType.QUERY
)
json_required_alnum_str = partial(
    validate_alnum_str, required=True, request_type=RequestType.BODY
)
query_required_alnum_str = partial(
    validate_alnum_str, required=True, request_type=RequestType.QUERY
)
json_optional_alnum_str = partial(
    validate_alnum_str, required=False, request_type=RequestType.BODY
)
query_optional_alnum_str = partial(
    validate_alnum_str, required=False, request_type=RequestType.QUERY
)
json_required_latitude = partial(
    validate_latitude, required=True, request_type=RequestType.BODY
)
query_required_latitude = partial(
    validate_latitude, required=True, request_type=RequestType.QUERY
)
json_optional_latitude = partial(
    validate_latitude, required=False, request_type=RequestType.BODY
)
query_optional_latitude = partial(
    validate_latitude, required=False, request_type=RequestType.QUERY
)
json_required_datetime = partial(
    validate_datetime, required=True, request_type=RequestType.BODY
)
query_required_datetime = partial(
    validate_datetime, required=True, request_type=RequestType.QUERY
)
json_optional_datetime = partial(
    validate_datetime, required=False, request_type=RequestType.BODY
)
query_optional_datetime = partial(
    validate_datetime, required=False, request_type=RequestType.QUERY
)
json_required_date = partial(
    validate_date, required=True, request_type=RequestType.BODY
)
query_required_date = partial(
    validate_date, required=True, request_type=RequestType.QUERY
)
json_optional_date = partial(
    validate_date, required=False, request_type=RequestType.BODY
)
query_optional_date = partial(
    validate_date, required=False, request_type=RequestType.QUERY
)
json_required_time = partial(
    validate_time, required=True, request_type=RequestType.BODY
)
query_required_time = partial(
    validate_time, required=True, request_type=RequestType.QUERY
)
json_optional_time = partial(
    validate_time, required=False, request_type=RequestType.BODY
)
query_optional_time = partial(
    validate_time, required=False, request_type=RequestType.QUERY
)
