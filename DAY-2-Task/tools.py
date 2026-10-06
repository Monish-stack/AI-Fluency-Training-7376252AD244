from scenario import LAPTOPS


def get_laptop_details(name):
    """Return information about a laptop."""

    if name not in LAPTOPS:
        return f"Laptop '{name}' was not found."

    return LAPTOPS[name]