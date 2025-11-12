# Goal: Create and reuse helper functions to solve a bigger logic problem.
#
# Write:
#
# is_prime(n) — returns True if n is prime.
# list_primes(start, end) — returns a list of all primes between start and end.
# Ask the user for the range and:
#
# Show the primes,
# Count them,
# Print the average distance between consecutive primes.
# Example:
#
# Range: 10–50
# Primes: 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47
# Count: 11
# Average gap: 3.6


def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True


def list_primes(start, end):
    primes = []
    for num in range(start, end):
        if is_prime(num):
            primes.append(num)
    return primes

a = input("Enter the range (make a space): ").split()
a[0] = int(a[0])
a[1] = int(a[1])
lst_primes =list_primes(a[0],a[1])
gaps = []
for i in range(1, len(lst_primes)):
    gaps.append(lst_primes[i]-lst_primes[i-1])
average = sum(gaps) / len(gaps)

print(f"Range: {a[0]}-{a[1]}\nPrimes: {lst_primes}\nCount: {len(lst_primes)}\nAverage gap:{average: .2f}")
