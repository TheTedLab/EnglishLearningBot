import random


def divide_dataset(dataset: str):
    with open(dataset, "r") as f:
        data = f.read().split('\n')

    random.shuffle(data)

    train_data = "\n"
    test_data = "\n"

    boarder = len(data)*4/5
    print(boarder)

    with open("train.csv", "w") as f:
        f.write(train_data.join(data[:int(boarder)]))

    with open("test.csv", "w") as f:
        f.write(test_data.join(data[int(boarder):]))
