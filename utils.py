def chunk(lst, partLength):
    lstSize = len(lst)
    chunksAmount = lstSize / partLength

    for i in chunksAmount:
        print(lst[:chunksAmount])