def to_number(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


def get_value(packet, column):
    value = packet.copy()

    for col in column.split('.'):
        if hasattr(value, '__iter__'):
            value = value.get(col)
        else:
            value = None

    return value
