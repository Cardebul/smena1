class MinHourLimited(Exception):
    pass

def valid_hour(value):
    if value < 144 :
        raise MinHourLimited
    return True