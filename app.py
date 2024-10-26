from validate import (
    validate_int,
    validate_latitude,
    validate_datetime,
    validate_date,
    validate_time,
    validate_alnum_str,
)


errors = {}

# キーが存在しない
assert validate_int(errors, {"unknown": "123"}, "any", min=100, max=200) is False
# 正しい整数の判定
assert (
    validate_int(errors, {"number_001": "123"}, "number_001", min=100, max=200) is True
)
# 正しい整数の判定
assert validate_int(errors, {"number_002": 123}, "number_002", min=100, max=200) is True
# 整数の範囲外
assert (
    validate_int(errors, {"number_003": "22"}, "number_003", min=100, max=200) is False
)
# 整数の範囲外
assert validate_int(errors, {"number_004": 22}, "number_004", min=100, max=200) is False
# 整数ではなく、小数
assert (
    validate_int(errors, {"number_005": "22.0"}, "number_005", min=100, max=200)
    is False
)
# 全角数字
assert validate_int(errors, {"number_006": "１２３"}, "number_006") is False
# 数値以外の型を受けた
assert validate_int(errors, {"number_007": True}, "number_007") is False
# 負の数
assert validate_int(errors, {"number_008": "-123"}, "number_008") is True
assert validate_int(errors, {"number_009": -123}, "number_009") is True
# 16進数
assert validate_int(errors, {"number_010": "FACE"}, "number_010") is False
# 正の小数
assert validate_latitude(errors, {"latitude_001": "12"}, "latitude_001") is True
# 正の小数
assert validate_latitude(errors, {"latitude_002": "12.3"}, "latitude_002") is True
# 正の小数
assert validate_latitude(errors, {"latitude_003": 12}, "latitude_003") is True
# 正の小数
assert validate_latitude(errors, {"latitude_004": 12.3}, "latitude_004") is True
# 小数ではない文字列
assert validate_latitude(errors, {"latitude_005": "12.3.4"}, "latitude_005") is False
# 緯度の範囲外の値
assert validate_latitude(errors, {"latitude_006": "91"}, "latitude_006") is False
# 緯度の範囲外の値
assert validate_latitude(errors, {"latitude_007": "-91"}, "latitude_007") is False
# 非値文字列
assert validate_latitude(errors, {"latitude_008": "nan"}, "latitude_008") is False
# 全角数字
assert validate_latitude(errors, {"latitude_009": "１２"}, "latitude_009") is False
# 数値以外の型を受けた
assert validate_latitude(errors, {"latitude_010": True}, "latitude_010") is False
# 非値
assert (
    validate_latitude(errors, {"latitude_011": float("nan")}, "latitude_011") is False
)
# 正しいISO8601の日時
assert (
    validate_datetime(errors, {"datetime_001": "2021-01-01T00:00:00"}, "datetime_001")
    is True
)
# 時間のない日付
assert (
    validate_datetime(errors, {"datetime_002": "2021-01-01"}, "datetime_002") is False
)
# 範囲外の日時
assert (
    validate_datetime(errors, {"datetime_003": "2020-01-01T00:00:00"}, "datetime_003")
    is False
)
# 存在しない日時
assert (
    validate_datetime(errors, {"datetime_004": "2021-01-32T00:00:00"}, "datetime_004")
    is False
)
# 正しいISO8601の日付
assert validate_date(errors, {"date_001": "2021-01-01"}, "date_001") is True
# 存在しない日付
assert validate_date(errors, {"date_002": "2021-01-32"}, "date_002") is False
# 範囲外の日付
assert validate_date(errors, {"date_003": "2020-01-01"}, "date_003") is False
# 日付に対して日時
assert validate_date(errors, {"date_004": "2021-01-01T00:00:00"}, "date_004") is False
# 正しいISO8601の時間
assert validate_time(errors, {"time_001": "12:00:00"}, "time_001") is True
# 時間に対して日時
assert validate_time(errors, {"time_002": "2021-01-01T00:00:00"}, "time_002") is False
# 正しい文字列
assert validate_alnum_str(errors, {"alnum_str_001": "abc123"}, "alnum_str_001") is True
# 空文字
assert validate_alnum_str(errors, {"alnum_str_002": ""}, "alnum_str_002") is False
# 全角文字
assert (
    validate_alnum_str(errors, {"alnum_str_003": "あいうえお"}, "alnum_str_003")
    is False
)
# 記号
assert (
    validate_alnum_str(errors, {"alnum_str_004": "abc123!"}, "alnum_str_004") is False
)

print(errors)
