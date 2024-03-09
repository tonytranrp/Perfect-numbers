import time
import math
import multiprocessing
import concurrent.futures

def precompute_primes(prime_limit):
    """ Precompute primes up to a given limit """
    sieve = [True] * (prime_limit // 2)
    for i in range(3, math.isqrt(prime_limit) + 1, 2):
        if sieve[i // 2]:
            sieve[i*i // 2::i] = [False] * ((prime_limit - i*i - 1) // (2*i) + 1)
    return [2] + [2 * i + 1 for i in range(1, prime_limit // 2) if sieve[i]]

def primes(n):
    """ Return a list of primes < n """
    if n <= 2:
        return []
    sieve = [True] * (n//2)
    limit = math.ceil(math.sqrt(n)) + 1
    for i in range(3, limit, 2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n - i*i - 1) // (2*i) + 1)
    return [2] + [2*i + 1 for i in range(1, n//2) if sieve[i]]

def lucas_lehmer(p):
    ''' The Lucas-Lehmer primality test for Mersenne primes.
        See https://en.wikipedia.org/wiki/Mersenne_prime#Searching_for_Mersenne_primes
    '''
    m = (1 << p) - 1
    s = 4
    for i in range(p - 2):
        s = (s * s - 2) % m
    return s == 0 and m or 0

def find_perfect_numbers(primes_list):
    perfect_numbers = []
    for p in primes_list:
        m = lucas_lehmer(p)
        if m:
            n = m << (p - 1)
            perfect_number = n * (n + 1) // 2
            perfect_numbers.append(str(perfect_number))
    return perfect_numbers

def main():
    filename = "perfect_numbers.txt"
    count = 0
    start_time = time.time()

    # Precompute primes
    prime_limit = 9973
    primes_list = precompute_primes(prime_limit)

    # Split primes list into chunks for multiprocessing
    num_processes = multiprocessing.cpu_count()
    chunk_size = len(primes_list) // num_processes

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = executor.map(find_perfect_numbers, [primes_list[i:i+chunk_size] for i in range(0, len(primes_list), chunk_size)])
        perfect_numbers = [num for sublist in results for num in sublist]

    # Write perfect numbers to file
    with open(filename, "w") as file:
        file.write("\n".join(perfect_numbers))

    count = len(perfect_numbers)
    end_time = time.time()
    print("Total perfect numbers found:", count)
    print("Perfect numbers written to", filename)
    print("Time taken:", end_time - start_time, "seconds")

if __name__ == "__main__":
    main()
