from datetime import datetime

from app import functions


def test_zip_code_validate():
    assert functions.validate_zip_code("12-345") is True
    assert functions.validate_zip_code("12345") is True
    assert functions.validate_zip_code("123456") is False
    assert functions.validate_zip_code("aa-bbb") is False


def test_date_and_time_validate():
    proper_date = datetime(year=2050, month=10, day=10, hour=10, minute=10)
    improper_date1 = datetime(year=2000, month=10, day=10, hour=10, minute=10)
    improper_date2 = datetime(year=2050, month=12, day=10, hour=23, minute=10)
    improper_date3 = datetime(year=2050, month=12, day=10, hour=6, minute=10)

    assert functions.validate_date_and_time(
        proper_date.date(), proper_date.time()
    ) is True
    assert functions.validate_date_and_time(
        improper_date1.date(), improper_date1.time()
    ) is False
    assert functions.validate_date_and_time(
        improper_date2.date(), improper_date2.time()
    ) is False
    assert functions.validate_date_and_time(
        improper_date3.date(), improper_date3.time()
    ) is False
