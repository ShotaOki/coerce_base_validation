from validate import (
    validate_int,
    validate_latitude,
    validate_datetime,
    validate_date,
    validate_time,
)


errors = {}

validate_int(errors, {"unknown": "123"}, "any", min=100, max=200)
validate_int(errors, {"number_001": "123"}, "number_001", min=100, max=200)
validate_int(errors, {"number_002": 123}, "number_002", min=100, max=200)
validate_int(errors, {"number_003": "22"}, "number_003", min=100, max=200)
validate_int(errors, {"number_004": 22}, "number_004", min=100, max=200)
validate_int(errors, {"number_005": "22.0"}, "number_005", min=100, max=200)
validate_int(errors, {"number_006": "１２３"}, "number_006")
validate_int(errors, {"number_007": True}, "number_007")
validate_int(errors, {"number_008": "-123"}, "number_008")
validate_latitude(errors, {"latitude_001": "12"}, "latitude_001")
validate_latitude(errors, {"latitude_002": "12.3"}, "latitude_002")
validate_latitude(errors, {"latitude_003": 12}, "latitude_003")
validate_latitude(errors, {"latitude_004": 12.3}, "latitude_004")
validate_latitude(errors, {"latitude_005": "12.3.4"}, "latitude_005")
validate_latitude(errors, {"latitude_006": "91"}, "latitude_006")
validate_latitude(errors, {"latitude_007": "-91"}, "latitude_007")
validate_latitude(errors, {"latitude_008": "nan"}, "latitude_008")
validate_latitude(errors, {"latitude_009": "１２"}, "latitude_009")
validate_datetime(errors, {"datetime_001": "2021-01-01T00:00:00"}, "datetime_001")
validate_datetime(errors, {"datetime_002": "2021-01-01"}, "datetime_002")
validate_datetime(errors, {"datetime_003": "2020-01-01T00:00:00"}, "datetime_003")
validate_date(errors, {"date_001": "2021-01-01"}, "date_001")
validate_date(errors, {"date_002": "2021-01-32"}, "date_002")
validate_date(errors, {"date_003": "2020-01-01"}, "date_003")
validate_date(errors, {"date_004": "2021-01-01T00:00:00"}, "date_004")
validate_time(errors, {"time_001": "12:00:00"}, "time_001")
validate_time(errors, {"time_002": "2021-01-01T00:00:00"}, "time_002")

print(errors)
