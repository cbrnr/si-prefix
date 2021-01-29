from math import log10


PREFIXES = {
    24: ["Y", "yotta"],
    21: ["Z", "zetta"],
    18: ["E", "exa"],
    15: ["P", "peta"],
    12: ["T", "tera"],
    9: ["G", "giga"],
    6: ["M", "mega"],
    3: ["k", "kilo"],
    2: ["h", "hecto"],
    1: ["da", "deca"],
    0: [""],
    -1: ["d", "deci"],
    -2: ["c", "centi"],
    -3: ["m", "milli"],
    -6: ["μ", "µ", "u", "micro"],
    -9: ["n", "nano"],
    -12: ["p", "pico"],
    -15: ["f", "femto"],
    -18: ["a", "atto"],
    -21: ["z", "zepto"],
    -24: ["y", "yocto"]
}


def siprefix(number, prefix="auto", ten_hundred=False):
    """Return the number scaled according to the specified SI prefix.

    By default, numbers are scaled so that they are always greater than or
    equal to 1, but less than the value corresponding to the next available
    prefix.

    Parameters
    ----------
    number : numeric
        Input number to convert.
    prefix : str
        SI prefix for scaling the number; if "auto", select best prefix
        automatically.
    ten_hundred : bool
        Whether to include the (less commonly used) prefixes for 10 (da, deka),
        100 (h, hecto), 1/10 (d, deci), and 1/100 (c, centi).

    Returns
    -------
    value : float
        Number scaled to match the SI prefix.
    prefix : str
        Selected SI prefix.

    Examples
    --------
    >>> siprefix(10)
    (10.0, '')
    >>> siprefix(10, ten_hundred=True)
    (1.0, 'da')
    >>> siprefix(2000)
    (2.0, 'k')
    >>> siprefix(54611234.8)
    (54.6112348, 'M')
    >>> siprefix(0.033)
    (33.0, 'm')
    >>> siprefix(22.3e-6)
    (22.3, 'μ')
    >>> siprefix(22.3e-6, "n")
    (22300.0, 'n')

    Notes
    -----
    Due to limited precision of floating point numbers, minor differences
    between the original input and the scaled output are expected.
    """
    if number == 0:
        return number, ""
    if prefix == "auto":  # determine best SI prefix automatically
        index = round(log10(abs(number)))
        min_index = min(PREFIXES.keys())
        while index >= min_index:
            p = PREFIXES.get(index)
            if p is None or (not ten_hundred and index in [2, 1, -1, -2]):
                index -= 1
            else:
                return number / 10**index, p[0]
        return number / 10**min_index, PREFIXES.get(min_index)[0]
    else:  # use provided SI prefix
        index = {i: k for k, v in PREFIXES.items() for i in v}[prefix]
        return number / 10**index, PREFIXES[index][0]
