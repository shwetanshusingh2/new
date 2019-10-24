i = 1
while i != 101:
    with open("numbers/{}.txt".format(i), "w+") as file:
        file.write("{}".format(i))
        i = i + 1
