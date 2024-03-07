quick and dirty but fully automated benchmark page generator

not included: make your benchmarks more consistent by disabling SMT, isolating CPUs, disabling turbo boost and frequency scaling, sending interrupts to CPUs other than the CPUs running the benchmark, etc. It turns out that even after you do all this you get a significant amount of variance because of the large volume of syscalls and apparent nondeterminism of javascript runtimes.
