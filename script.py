import os


def change(path):
    ls = os.listdir(path)

    for fn in ls:
        if fn == ".DS_Store":
            continue
        mm = fn[0:2]
        dd = fn[3:5]
        os.rename(path + "/" + fn, path + "/" + "2020" + "-" + mm + "-" + dd + ".csv")


change("res/NYT/Sports")
change("res/NYT/Opinion")
change("res/NYT/Politics")
change("res/NYT/Science")
change("res/NYT/Business")

change("res/Guardian/Sport")
change("res/Guardian/Opinion")
change("res/Guardian/Politics")
change("res/Guardian/Science")
change("res/Guardian/Business")

