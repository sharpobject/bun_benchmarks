import json
import matplotlib.pyplot as plt
import os
from math import log, exp

def generate_graph(benchmark_name, data, output_dir):
    plt.figure(figsize=(6, 4))
    plt.plot(data.keys(), data.values(), marker='o')
    plt.xlabel('Bun Version')
    plt.ylabel('Time (seconds)')
    plt.title(benchmark_name)
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=8)
    plt.grid(True)
    plt.tight_layout()
    
    # Create the subdirectory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the graph image in the specified directory
    plt.savefig(f'{output_dir}/{benchmark_name}.png', dpi=150)
    plt.close()

def generate_geometric_mean_graph(geometric_mean_data, output_dir):
    plt.figure(figsize=(6, 4))
    plt.plot(geometric_mean_data.keys(), geometric_mean_data.values(), marker='o')
    plt.xlabel('Bun Version')
    plt.ylabel('Geometric Mean Time (seconds)')
    plt.title('Geometric Mean Benchmark Time')
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=8)
    plt.grid(True)
    plt.tight_layout()
    
    # Create the subdirectory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the graph image in the specified directory
    plt.savefig(f'{output_dir}/geometric_mean.png', dpi=150)
    plt.close()

def generate_html(benchmarks, geometric_mean_data):
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Benchmark Results for bun-linux-x64 on Haswell</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            h1 {
                text-align: center;
            }
            .graph-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }
            .graph {
                width: 30%;
                margin: 10px;
                text-align: center;
            }
            .graph img {
                max-width: 100%;
                height: auto;
            }
            .graph h3 {
    font-size: 14px;
    margin-bottom: 5px;
}

        </style>
    </head>
    <body>
        <h1>Benchmark Results for bun-linux-x64 on Haswell</h1e>
        <div class="graph-container">
    '''
    html += f'''
    <div class="graph">
        <h3>Geometric mean benchmark time</h3>
        <img src="graphs/geometric_mean.png" alt="Geometric mean">
    </div>
    '''

    for benchmark_name, results in benchmarks.items():
        for result_name in results:
            html += f'''
            <div class="graph">
                <h3>{result_name}</h3>
                <img src="graphs/{benchmark_name}/{result_name}.png" alt="{result_name}">
            </div>
            '''

    html += f'''
        </div>
    </body>
    </html>
    '''

    with open('benchmark_results.html', 'w') as file:
        file.write(html)

def calculate_geometric_mean(data):
    log_sum = sum(log(time) for time in data.values())
    return exp(log_sum / len(data))

def main():
    # Load cache from JSON file
    with open("cache.json") as f:
        cache = json.load(f)

    # Create a directory for storing the graphs
    os.makedirs('graphs', exist_ok=True)

    # Generate graphs for each benchmark
    benchmarks = {}
    geometric_mean_data = {}
    for version in cache:
        version_data = []
        for benchmark_name, results in cache[version].items():
            if benchmark_name not in benchmarks:
                benchmarks[benchmark_name] = {}
            for result_name, time in results.items():
                if result_name not in benchmarks[benchmark_name]:
                    benchmarks[benchmark_name][result_name] = {}
                benchmarks[benchmark_name][result_name][version] = time
                version_data.append(time)
        geometric_mean_data[version] = calculate_geometric_mean(dict(zip(range(len(version_data)), version_data)))

    for benchmark_name, results in benchmarks.items():
        for result_name, data in results.items():
            output_dir = f"graphs/{benchmark_name}"
            generate_graph(result_name, data, output_dir)

    # Generate geometric mean graph
    generate_geometric_mean_graph(geometric_mean_data, "graphs")

    # Generate HTML file
    generate_html(benchmarks, geometric_mean_data)

if __name__ == "__main__":
    main()
