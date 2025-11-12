celsius = [-10, -5, 0, 12.5, 23.1, 35, 41, 100, 250, 300, 420]
print(f"Celsius | Fahrenheit\n--------|-----------")

for i in celsius:
    b = i * 1.8 + 32
    print(f"{i:7}", '|' , f"{int(b):7}")

res=[]
def c_to_f(celsius):
    for i in celsius:
        f = i * 9 / 5 + 32
        res.append(f)


    return res


def f_to_c(res):
    for t in res:
        a = (t - 32) * (5/9)
        print(f"{int(t):9}  | {int(a):3}")



print("\nFahrenheit | Celsius\n-----------|--------- ")
f = c_to_f(celsius)


a = f_to_c(res)