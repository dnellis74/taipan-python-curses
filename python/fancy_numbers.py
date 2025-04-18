def fancy_numbers(num: float) -> str:
    """
    Format numbers in a fancy way, converting large numbers to millions with decimal points.
    Returns the formatted string.
    """
    if num >= 100000000:
        num1 = int(num / 1000000)
        return f"{num1} Million"
    elif num >= 10000000:
        num1 = int(num / 1000000)
        num2 = int((int(num) % 1000000) / 100000)
        if num2 > 0:
            return f"{num1}.{num2} Million"
        else:
            return f"{num1} Million"
    elif num >= 1000000:
        num1 = int(num / 1000000)
        num2 = int((int(num) % 1000000) / 10000)
        if num2 > 0:
            return f"{num1}.{num2} Million"
        else:
            return f"{num1} Million"
    else:
        return str(int(num))