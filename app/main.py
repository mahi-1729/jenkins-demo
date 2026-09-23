def add(a, b):
    return a + b


def get_message():
    return "Hello from Jenkins CI!"


if __name__ == "__main__":
    print(get_message())
    print("2 + 3 =", add(2, 3))
