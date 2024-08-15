import os
import multiprocessing as mp


def get_line_chunks(file_name: str, max_cpu: int = 8) -> tuple[int, list[tuple[str, int, int]]]:
    cpu_count = min(max_cpu, mp.cpu_count())

    # Рахуємо тепер чанки не за допомогою байтів, а кількістю рядків
    with open(file_name, encoding="utf-8", mode="r") as f:
        total_lines = sum(1 for _ in f)

    chunk_size = total_lines // cpu_count

    start_end = []
    start_line = 0
    while start_line < total_lines:
        end_line = min(total_lines, start_line + chunk_size)
        start_end.append((file_name, start_line, end_line))
        start_line = end_line

    return cpu_count, start_end


def _process_file_chunk(file_name: str, start_line: int, end_line: int) -> dict:
    result = {}
    with open(file_name, encoding="utf-8", mode="r") as f:
        # Замість того, щоб передавати самі рядки з текстом, передаємо діапазон індексів рядків
        for i, line in enumerate(f):
            if i < start_line:
                continue
            if i >= end_line:
                break
            location, measurement = line.split(";")
            measurement = float(measurement)
            _result = result.get(location)
            if _result:
                if measurement < _result[0]:
                    _result[0] = measurement
                if measurement > _result[1]:
                    _result[1] = measurement
                _result[2] += measurement
                _result[3] += 1
            else:
                result[location] = [measurement, measurement, measurement, 1]

    return result


def process_file(cpu_count: int, start_end: list) -> dict:
    with mp.Pool(cpu_count) as p:
        chunk_results = p.starmap(_process_file_chunk, start_end)

    result = {}
    for chunk_result in chunk_results:
        for location, measurements in chunk_result.items():
            _result = result.get(location)
            if _result:
                if measurements[0] < _result[0]:
                    _result[0] = measurements[0]
                if measurements[1] > _result[1]:
                    _result[1] = measurements[1]
                _result[2] += measurements[2]
                _result[3] += measurements[3]
            else:
                result[location] = measurements

    print("{", end="")
    for location, measurements in sorted(result.items()):
        print(
            f"{location}={measurements[0]:.1f}/{(measurements[2] / measurements[3]) if measurements[3] != 0 else 0:.1f}/{measurements[1]:.1f}",
            end=", ",
        )
    print("\b\b} ")


if __name__ == "__main__":
    cpu_count, start_end = get_line_chunks("measurements.txt")
    process_file(cpu_count, start_end)
