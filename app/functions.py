from datetime import datetime, time, timedelta


def get_tomorrow():
    return datetime.today().date() + timedelta(days=1)


def extract(data, symbols_list=[]):
    return "".join([d for d in data if (d.isdigit() or d in symbols_list)])


def validate_date_and_time(input_date, input_time):
    start_hour = time(9, 0)
    close_hour = time(20, 0)

    try:
        if input_date >= get_tomorrow() and start_hour < input_time < close_hour:
            return True

    except ValueError as e:
        print(e)
        return False


def validate_zip_code(data):
    code = extract(data, ["-"])
    if '-' in code:
        code_array = code.split("-")
        if len(extract(code_array[0])) == 2 and len(extract(code_array[1])) == 3:
            return True
    return len(extract(code)) == 5


def validate_phone_number(data):
    polish_prefixes = ["12", "13", "14", "15", "16", "17", "18", "22", "23", "24", "25", "29", "32", "33", "34",
                       "41", "42", "43", "44", "46", "48", "52", "54", "55", "56", "58", "59", "61", "62", "63",
                       "65", "67", "68", "71", "74", "75", "76", "77", "81", "82", "83", "84", "85", "86", "87",
                       "89", "91", "94", "95"] + ["50", "51", "53", "57", "60", "66", "69", "72", "73",
                                                  "78", "79", "88"]
    phone_number = extract(data, ["+"])
    return 12 <= len(phone_number) <= 13 and phone_number[1:3] in polish_prefixes
