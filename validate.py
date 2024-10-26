from input_coerce import input_coerce, TypeCheck
from datetime import datetime, date, time
from math import isfinite

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
    [
        # クエリ文字列: 型はString、バリデータ関数の中ではintとして扱う
        TypeCheck(input_type=str, coerce=int, regex=REGEX_SIGNED_INT),
        # JSONボディ: 型はNumber、バリデータ関数の中ではintとして扱う
        TypeCheck(input_type=number_type, coerce=int),
    ]
)
def validate_int(
    error: dict,
    input: dict,
    key: str,
    min: int = None,
    max: int = None,
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
    [
        # クエリ文字列: 型はString、バリデータ関数の中ではStringとして扱う
        # 空文字はpre_validateで許容しない
        TypeCheck(
            input_type=str,
            coerce=str,
            regex=REGEX_ALNUM,
            pre_validate=lambda x: len(x) >= 1,
        ),
    ]
)
def validate_alnum_str(
    error: dict,
    input: dict,
    key: str,
    coerced: str = None,
):
    return True


@input_coerce(
    [
        # クエリ文字列: 型はString、バリデータ関数の中では有限のfloatとして扱う
        TypeCheck(
            input_type=str, coerce=float, regex=REGEX_FLOAT, pre_validate=isfinite
        ),
        # JSONボディ: 型はNumber、バリデータ関数の中では有限のfloatとして扱う
        TypeCheck(input_type=number_type, coerce=float, pre_validate=isfinite),
    ]
)
def validate_latitude(
    error: dict,
    input: dict,
    key: str,
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
    [
        # クエリ、JSON共通
        # 型はString、バリデータ関数の中ではdatetimeとして扱う
        TypeCheck(
            input_type=str,
            coerce=datetime,
            coerce_function=datetime.fromisoformat,
            regex=REGEX_DATETIME,
        ),
    ]
)
def validate_datetime(
    error: dict,
    input: dict,
    key: str,
    coerced: datetime = None,
):
    if coerced.year < 2021:
        error[key] = f"{key} is less than 2021"
        return False
    return True


@input_coerce(
    [
        # クエリ、JSON共通
        # 型はString、バリデータ関数の中ではdateとして扱う
        TypeCheck(
            input_type=str,
            coerce=date,
            coerce_function=date.fromisoformat,
            regex=REGEX_DATE,
        ),
    ]
)
def validate_date(
    error: dict,
    input: dict,
    key: str,
    coerced: date = None,
):
    if coerced.year < 2021:
        error[key] = f"{key} is less than 2021"
        return False
    return True


@input_coerce(
    [
        # クエリ、JSON共通
        # 型はString、バリデータ関数の中ではtimeとして扱う
        TypeCheck(
            input_type=str,
            coerce=time,
            coerce_function=time.fromisoformat,
            regex=REGEX_TIME,
        ),
    ]
)
def validate_time(
    error: dict,
    input: dict,
    key: str,
    coerced: time = None,
):
    if coerced.hour < 6:
        error[key] = f"{key} is less than 6"
        return False
    return True
