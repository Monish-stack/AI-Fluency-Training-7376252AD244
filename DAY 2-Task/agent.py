from tools import get_laptop_details


def agent(question, max_steps=8):

    laptops = ["Laptop A", "Laptop B", "Laptop C"]

    print("\nTHOUGHT:")
    print("I need the price, discount, RAM, and storage of all laptops "
          "before I can determine which has the lowest discounted price.")

    observations = {}

    for laptop in laptops:

        print("\nACTION:")
        print(f"get_laptop_details({laptop})")

        result = get_laptop_details(laptop)
        observations[laptop] = result

        print("\nOBSERVATION:")
        print(result)

    # Extract the values from the tool results
    final_prices = {}

    for laptop, data in observations.items():
        price = data["price"]
        discount = data["discount"]

        discounted_price = price * (1 - discount / 100)

        final_prices[laptop] = discounted_price

    lowest_laptop = min(final_prices, key=final_prices.get)
    lowest_price = final_prices[lowest_laptop]

    specs = observations[lowest_laptop]

    print("\nTHOUGHT:")
    print("I retrieved all three laptops. I calculated each discounted "
          "price and compared them.")

    print("\nCALCULATIONS:")

    for laptop, price in final_prices.items():
        print(f"{laptop}: Rs. {price:,.2f}")

    print("\nFINAL:")
    print(
        f"{lowest_laptop} has the lowest discounted price of "
        f"Rs. {lowest_price:,.2f}. "
        f"It has {specs['ram']} RAM and {specs['storage']} storage."
    )

    return (
        f"{lowest_laptop} has the lowest discounted price of "
        f"Rs. {lowest_price:,.2f}, with {specs['ram']} RAM "
        f"and {specs['storage']} storage."
    )