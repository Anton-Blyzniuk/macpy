def fit_number_in_range_or_raise_an_error(
        lower_bound: int|float,
        upper_bound: int|float,
        number: float|int,
        raise_on_error: bool=None,
) -> int|float:
    if number < lower_bound:
        if raise_on_error:
            raise Exception(
                f"Number {number} is out of range. Lower bound is {lower_bound}"
            )
        return lower_bound

    elif number > upper_bound:
        if raise_on_error:
            raise Exception(
                f"Number {number} is out of range. Upper bound is {upper_bound}"
            )
        return upper_bound

    return number
