import random


def random_string(length):
    chars = []
    for i in range(length):
        chars.append(chr(random.randint(0, 255)))
    return "".join(chars)


if __name__ == "__main__":
    random.seed(0)
    file = open("small_random.txt", "w", encoding='utf-8')
    file.write(random_string(100))
    file.close()

    random.seed(1)
    file = open("medium_random.asc", "w", encoding='utf-8')
    file.write(random_string(1000))
    file.close()

    random.seed(2)
    file = open("large_random.txt", "w", encoding='utf-8')
    file.write(random_string(10000))
    file.close()
