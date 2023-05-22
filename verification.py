def verify_ico(ico:str) -> bool:
    ico = str(ico).zfill(8)  # ensure ico is 8 digits long, fill with zeroes if necessary
    if len(ico) != 8 or not ico.isdigit():
        return False

    weights = [8, 7, 6, 5, 4, 3, 2]
    weighted_sum = sum([int(ico[i]) * weights[i] for i in range(7)])  # calculate weighted sum of the first 7 digits

    x = (11 - (weighted_sum % 11)) % 10

    return x == int(ico[7])  


def main():
    pass

if __name__ == "__main__":
    main()