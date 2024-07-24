import argparse
import time
from concurrent.futures import ThreadPoolExecutor


def cpu_bound_task(n):
    """A CPU-bound task that computes the sum of squares up to n."""
    return sum(i * i for i in range(n))


def main():
    parser = argparse.ArgumentParser(
        description="Run a CPU-bound task with threads")
    parser.add_argument("--threads", type=int, default=4,
                        help="Number of threads")
    parser.add_argument("--tasks", type=int, default=10,
                        help="Number of tasks")
    parser.add_argument(
        "--size", type=int, default=5000000, help="Task size (n for sum of squares)"
    )
    args = parser.parse_args()

    print(f"Running {args.tasks} tasks of size {
          args.size} with {args.threads} threads")

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        list(executor.map(cpu_bound_task, [args.tasks] * args.size))
    end_time = time.time()
    duration = end_time - start_time

    print(f"Time with threads: {duration:.2f} seconds")


if __name__ == "__main__":
    main()
