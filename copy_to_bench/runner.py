import json
import os
import re
import subprocess
from collections import defaultdict

def run_benchmark(bun_version, benchmark):
    command = f"taskset -c 4-7 /home/ltcm-admin/buns/bun_releases/bun-v{bun_version}/bun-linux-x64/bun run {benchmark}"
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    return output

def extract_benchmarks(outputs):
    benchmarks = defaultdict(lambda:0.0)
    for output in outputs:
        pattern = r"^(.*?)\s+([\d.]+)\s*(ns|µs|ms|s)/iter"
        matches = re.findall(pattern, output, re.MULTILINE)
        for match in matches:
            name = match[0].strip()
            value = float(match[1])
            unit = match[2]
            if unit == "ns":
                benchmarks[name] += value / 1e9
            elif unit == "µs":
                benchmarks[name] += value / 1e6
            elif unit == "ms":
                benchmarks[name] += value / 1e3
            else:
                benchmarks[name] += value
    for k in benchmarks:
        benchmarks[k] /= len(outputs)
    return benchmarks


def strip_color_codes(output):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', output)

def get_bun_versions():
    releases_dir = "/home/ltcm-admin/buns/bun_releases/"

    # Get the list of directories in the releases directory
    directories = [dir for dir in os.listdir(releases_dir) if os.path.isdir(os.path.join(releases_dir, dir))]

    # Sort the directories based on creation time (oldest first)
    sorted_directories = sorted(directories, key=lambda dir: os.path.getctime(os.path.join(releases_dir, dir)))

    # Extract the version numbers from the directory names
    versions = [dir.split("-v")[1] for dir in sorted_directories if dir.startswith("bun-v")]

    return versions

def main():
    # Load versions and benchmarks from JSON file
    with open("config.json") as f:
        config = json.load(f)
    benchmarks = config["benchmarks"]
    versions = get_bun_versions()

    # Load cache from JSON file
    try:
        with open("cache.json") as f:
            cache = json.load(f)
    except FileNotFoundError:
        cache = {}

    # Run benchmarks and update cache
    for version in versions:
        if version not in cache:
            cache[version] = {}
    for benchmark in benchmarks:
        for version in versions:
            if benchmark not in cache[version]:
                outputs = [run_benchmark(version, benchmark) for x in range(4)]
                outputs = [strip_color_codes(output) for output in outputs]
                benchmarks_data = extract_benchmarks(outputs)
                cache[version][benchmark] = benchmarks_data
                print(f"Benchmarks for {benchmark} on Bun v{version}:")
                for name, time in benchmarks_data.items():
                    print(f"- {name}: {time:.11f} seconds")

    # Save updated cache to JSON file
    with open("cache.json", "w") as f:
        json.dump(cache, f, indent=2)

if __name__ == "__main__":
    main()
