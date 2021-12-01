#! /bin/sh
cd aoc

cd go
echo "Go"
gotip run main.go $*

cd ..
echo "Python"
python3 -m python $*

echo "pypy"
PYENV_VERSION=pypy3.8-7.3.7 python -m python $*

cd rust
echo "Rust"
cargo run -q --release $*
