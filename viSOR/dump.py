
def dump_csv(file_name: str, parser: object):
    X = parser.X
    Y = parser.Y

    with open(file_name, 'w', newline='') as csvfile:
        for x, y in zip(X, Y):
            csvfile.write(f"{x},{y}\n")


def dump_tsv(file_name: str, parser: object):
    X = parser.X
    Y = parser.Y

    with open(file_name, 'w', newline='') as csvfile:
        for x, y in zip(X, Y):
            csvfile.write(f"{x}\t{y}\n")
