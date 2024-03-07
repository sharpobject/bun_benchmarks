#!/bin/bash

while true; do
    python3 runner.py
    python3 gen_page.py
    cp -r benchmark_results.html graphs ~/repos/bun_benchmarks
    pushd ~/repos/bun_benchmarks
    git add .
    git commit -m "automatic commit"
    git push origin master
    popd
done
