import platform
import statistics
import subprocess
import time

from pipeline import Condition, Item, Match, Pipeline, Transform

order_pipeline = Pipeline(
    customer_email={
        "type": str,
        "conditions": {
            Condition.MaxLength: 64
        },
        "matches": {
            Match.Format.Email: None
        },
        "transform": {
            Transform.Lowercase: None
        }
    },
    items={
        "type": list,
        "conditions":
            {
                Condition.MinLength: 1,
                Condition.MaxLength: 50,
                Item(Condition.IncludedIn): ["water", "sushi", "pizza"]
            }
    },
    total_amount={
        "type": float,
        "conditions": {
            Condition.MinNumber: 0.01,
            Condition.MaxNumber: 10000.00
        }
    },
    discount_code={
        "type": str,
        "conditions": {
            Condition.MaxLength: 20
        },
        "matches": {
            Match.Text.Alphanumeric: None
        },
        "transform": {
            Transform.Uppercase: None
        },
        "optional": True
    }
)

test_data = {
    "customer_email": "Customer@Example.com",
    "items": ["sushi", "pizza"],
    "total_amount": 99999.99,
    "discount_code": "save20"
}


def get_runtime() -> str:
    try:
        cmd = ["sysctl", "-n", "machdep.cpu.brand_string"]

        cpu: str = subprocess.check_output(cmd, stderr=subprocess.DEVNULL
                                          ).decode().strip()
    except:
        cpu: str = platform.processor() or platform.machine()

    os_info: str = platform.platform()

    python_version: str = platform.python_version()

    return f"Python {python_version} on {os_info} ({cpu})"


def run_benchmark(iterations: int) -> None:
    for _ in range(10_000):
        order_pipeline.run(data=test_data)

    execution_times: list[float] = []

    for _ in range(iterations):
        start: float = time.perf_counter()

        order_pipeline.run(data=test_data)

        execution_times.append((time.perf_counter() - start) * 1000)

    mean_time: float = statistics.mean(execution_times)
    median_time: float = statistics.median(execution_times)

    min_time: float = min(execution_times)
    max_time: float = max(execution_times)

    stdev_time: float = statistics.stdev(execution_times or [0, 0])

    throughput: float = 1000 / mean_time if mean_time > 0 else 0

    print(f"Runtime: {get_runtime()}")
    print(f"Iterations: {iterations}")
    print(f"Mean time: {mean_time:.4f} ms")
    print(f"Median time: {median_time:.4f} ms")
    print(f"Minimum time (Min): {min_time:.4f} ms")
    print(f"Maximum time (Max): {max_time:.4f} ms")
    print(f"Standard deviation (StDev): {stdev_time:.4f} ms")
    print(f"Throughput: {throughput:.2f} operations/second")


if __name__ == "__main__":
    run_benchmark(250_000)
