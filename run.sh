#! /bin/sh
cd aoc

cd go
echo "Go"
gotip run main.go $*

cd ..
echo "Python $(python3 -c 'import sys; print(sys.version.splitlines()[0])')"
python3 -m python $* 

echo "PyPy $(PYENV_VERSION="pypy3.8-7.3.7" python3 -c 'import sys; print(sys.version.splitlines()[0])')"
PYENV_VERSION="pypy3.8-7.3.7" python3 -m python $*

cd rust
echo "Rust"
cargo run -q --release $* 
