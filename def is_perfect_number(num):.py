import time
from multiprocessing import Pool, cpu_count

def sum_of_divisors(num):
    """
    Calculate the sum of divisors of a number.
    """
    if num <= 1:
        return 0
    
    divisors_sum = 1  # 1 is always a divisor
    sqrt_num = int(num ** 0.5)
    
    # Iterate over divisors up to the square root of num
    for i in range(2, sqrt_num + 1):
        if num % i == 0:
            # Add divisor and its corresponding divisor (if they are different)
            divisors_sum += i
            if i != num // i:
                divisors_sum += num // i
    
    return divisors_sum

def is_perfect_number(num):
    """
    Check if a number is a perfect number.
    """
    return sum_of_divisors(num) == num

def find_perfect_numbers(start, end):
    """
    Find perfect numbers within a specified range.
    """
    perfect_numbers = [num for num in range(start, end) if is_perfect_number(num)]
    return perfect_numbers

def main():
    limit = 1000000
    num_processes = cpu_count()
    chunk_size = limit // num_processes
    pool = Pool(processes=num_processes)
    
    start_time = time.time()
    results = pool.starmap(find_perfect_numbers, [(i, i + chunk_size) for i in range(2, limit, chunk_size)])
    perfect_numbers = [num for sublist in results for num in sublist]
    end_time = time.time()
    
    print("Time taken to find perfect numbers within limit:", end_time - start_time, "seconds")
    print("Perfect numbers within the limit of", limit, "are:", perfect_numbers)

if __name__ == "__main__":
    main()
