def number(num_string):
    if "." in num_string:
        return float(num_string)
    else:
        return int(num_string)

def value(val):
    return val