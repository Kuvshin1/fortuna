import datetime


def validate_datetime(value:str):
    try:
        datetime.datetime.fromisoformat(value)
    except ValueError:
        return False
    return True


def decode_to_primitive_type(value: str):
    # boolean
    if value in ['true', 'false']:
        return value == 'true'
    # datetime
    if validate_datetime(value):
        value = value.replace('t', 'T')
    return value