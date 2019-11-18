def fake_external_transfer_api(data):
    return True


def n_format(s, length):
    t = length / 3
    tmp = ''
    while t >= 0:
        tmp += s[0:3] + " "
        s = s[3:]
        t -= 1
    return tmp


def number_format(number):
    number = str(number)
    length = len(number)
    if length >= 4:
        m = length % 3
        if m == 0:
            return n_format(number, length)
        else:
            f_char = number[0:m]
            return f_char+" "+n_format(number[m:], len(number[m:]))
    else:
        return number
