#! /bin/sh
cd aoc

cd go
echo "Go"
gotip run main.go $*

cd ..
echo "Python"
python3 -m python $*

cd rust
echo "Rust"
cargo run -q --release $*
