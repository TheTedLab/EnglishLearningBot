import random


def divide_dataset():
    with open("dataset.txt", "r") as f:
        data = f.read().split('\n')

    random.shuffle(data)

    train_data = "\n"
    test_data = "\n"

    with open("train.csv", "w") as f:
        f.write(train_data.join(data[:200]))

    with open("test.csv", "w") as f:
        f.write(test_data.join(data[200:]))
