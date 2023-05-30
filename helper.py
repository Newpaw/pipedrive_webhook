import json
import logging


logging.basicConfig(
    format="[%(asctime)s +0000] [%(process)d] [%(levelname)s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def verify_ico(ico: str) -> bool:
    ico = str(ico).zfill(
        8
    )  # ensure ico is 8 digits long, fill with zeroes if necessary
    if len(ico) != 8 or not ico.isdigit():
        return False

    weights = [8, 7, 6, 5, 4, 3, 2]
    weighted_sum = sum(
        [int(ico[i]) * weights[i] for i in range(7)]
    )  # calculate weighted sum of the first 7 digits

    x = (11 - (weighted_sum % 11)) % 10

    return x == int(ico[7])


def different_and_correct_ico(data: json) -> bool:
    current_layer = data["current"].get("7d2ccc518c77ec9a5cefc1d88ef617bf8b005586")
    previous_layer = data["previous"].get("7d2ccc518c77ec9a5cefc1d88ef617bf8b005586")
    exist_the_ico = verify_ico(current_layer)

    logging.debug(f"The verification for IČ {current_layer} is {exist_the_ico}")

    if current_layer == previous_layer or not exist_the_ico:
        return False
    else:
        return True
    
def different_vat(data: json) -> bool:
    current_layer = data["current"].get("29d4a8de55841cc13da1337ea8fd4b3278868c68")
    previous_layer = data["previous"].get("29d4a8de55841cc13da1337ea8fd4b3278868c68")

    if current_layer == previous_layer and current_layer is not None:
        return False
    else:
        return True


def main():
    pass


if __name__ == "__main__":
    main()
