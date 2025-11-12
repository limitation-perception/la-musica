def get_min(numbers):
    return print(f"min = {min(numbers)}")
def get_max(numbers):

    return print(f"max = {max(numbers)}")

def get_average(numbers):
    summ = 0
    for i in numbers:
        summ += int(i)
    return summ / len(numbers)


def get_median(numbers):
    ln = len(numbers)
    sp = sorted(numbers)
    if ln % 2 == 0:
        ind1 = ln // 2 - 1
        ind2 = ln // 2
        return (sp[ind1] +sp[ind2]) / 2
    else:
        ind = ln//2
        return sp[ind]


a = input("Enter the list: ").split()
lst = []
for char in a:
    char = int(char)
    lst.append(char)
get_min(lst)
get_max(lst)
print(f"average = {get_average(lst)}")
print(f"median = {get_median(lst)}")