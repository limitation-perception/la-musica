def is_leap(year):
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        return True
    else:
        return False

def days_in_month(month, year):
    if month in [9,11,4,6]:
        return 30
    elif month in [1,3,5,7,8,10,12]:
        return 31
    else:
        if is_leap(year):
            return 29
        else:
            return 28

def next_month(month, year):
    if month == 12:
        return 1, year+1
    else:
        return month+1,year

def month_summary(month, year):
    month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
                   8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    month_name = month_names.get(month, "Unknown")
    days_count = days_in_month(month,year)
    leap_info = "(Leap Year: Yes)" if is_leap(year) else ""
    print(f"{month_name} {year} - {days_count} days {leap_info}")




def main():
    month = int(input("Enter month(number): "))
    year = int(input("Enter year: "))

    for i in range(3):
        month_summary(month, year)
        month, year = next_month(month,year)
main()
# print(is_leap(2024))
# print(days_in_month(2,2025))
# print(next_month(12,2024))
# month_summary(3,2024)