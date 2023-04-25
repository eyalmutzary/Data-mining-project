import json
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

with open('data.json', 'r') as file:
    data = json.load(file)


def put_in_list(data_type):
    type_list = []
    for d in data:
        try:
            if d[data_type]:
                type_list.append(d[data_type])
        except KeyError:
            pass
        except TypeError:
            pass
    return type_list


if __name__ == "__main__":
    budget_value = put_in_list("budget")
    print("max " + str(max(budget_value)))


    # b1
    sns.histplot(budget_value, kde=True)
    plt.xlabel('Budget (100 mil)')
    plt.ylabel('Number of Movies')
    plt.show()