import random
from net_constants import nb_classes


def divide_dataset(dataset: str):
    with open(dataset, "r") as f:
        data = f.read().split('\n')

    # random.shuffle(data)

    train_data = "\n"
    test_data = "\n"

    # boarder = len(data)*4/5
    # print(boarder)

    with open("sources/train.csv", "w") as f:
        f.write(train_data.join(data[:nb_classes * 10000]))

    with open("sources/test.csv", "w") as f:
        f.write(test_data.join(data[nb_classes * 10000:]))
