import random

def introduce_variation(objs, variation = 0):
    if variation > 0:
        varied_objs = [ (n, round((i+1-variation+2*variation*random.random()), 2)) for i, n in enumerate(objs)]
        objs = [ n[0] for n in sorted(varied_objs, key=lambda x: x[1])]
    return objs



if __name__ == "__main__":
    lst = [1,2,3,4,5,6,7,8,9,10]
    print(introduce_variation(lst, 3))