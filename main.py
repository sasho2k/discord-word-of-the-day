from client import *


"""The main function to call. """
if __name__ == '__main__':
    run()

"""
    date = ['2019', '1', '6']
    msg = wotd_flow(date)
    if (isinstance(msg, str)) and (msg.startswith("`ERROR ->")):
        print("ERROR!")
    else:
        print("SUCCESS!")
    exit(0)

    err = 0
    err_dates = []
    for n in range(2017, 2021):
        for e in range(1, 12):
            for i in range(1, 29):
                date = [n, e, i]
                msg = wotd_flow(date)
                if (isinstance(msg, str)) and (msg.startswith("`ERROR ->")):
                    err += 1
                    err_dates.append(date)
                else:
                    print("SUCCESS!")

    print(err)
    print(err_dates)
"""
