# FS Python Framework

## Requirements

`python3 -m pip install -U numpy scipy pandas matplotlib --user`

Define an environment variable `FS_FRAMEWORK` in `$HOME/.bashrc` or `$HOME/.profile` to point to the Python framework directory: `export FS_FRAMEWORK="$HOME/prospar-workspace/fs-python-framework/"`

## Examples

- One time activity: building m5 library for adding support to stat reset `cd $FS_FRAMEWORK; python3 src/main.py --tasks build_m5 --bench blackscholes --outputDir fs-test`

`cd $FS_FRAMEWORK; python3 src/main.py --tasks build_gem5 --trials 1 --bench blackscholes --verbose 1 --protocol FS_MESI --workloadSize small --outputDir fs-test`

`cd $FS_FRAMEWORK; python3 src/main.py --tasks run --trials 1 --bench blackscholes --verbose 1 --protocol FS_MESI --workloadSize small --outputDir fs-test --benchmark_type custom`

`cd $FS_FRAMEWORK; python3 src/main.py --tasks result --verbose 1 --outputDir 080622-fs-test`

## Test the generation of stats

- Copy the `test-demo` folder to the `prospar-exp-output` folder, the folder pointed by `[EXP_OUTPUT_ROOT]` in `config.ini`
- `cd $FS_FRAMEWORK; python3 src/main.py --tasks result --verbose 3 --outputDir test-demo`
- The output will be generated in the folder pointed by `[EXP_RESULT_ROOT]` in `config.ini`
