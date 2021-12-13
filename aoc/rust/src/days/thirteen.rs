use itertools::Itertools;

#[derive(Debug)]
struct Instruction {
    num: usize,
    along_x: bool,
}

type GRID = Vec<Vec<bool>>;

fn parse_input(input: &String) -> (GRID, Vec<Instruction>) {
    let (top, bottom) = input.split("\n\n").collect_tuple().unwrap();
    let points: Vec<(usize, usize)> = top
        .lines()
        .map(|l| {
            let (x, y) = l.split(",").collect_tuple().unwrap();
            (x.parse().unwrap(), y.parse().unwrap())
        })
        .collect_vec();

    let max_x = points.iter().map(|t| t.0).max().unwrap();
    let max_y = points.iter().map(|t| t.1).max().unwrap();
    let mut grid = Vec::new();
    for _ in 0..max_y + 1 {
        let mut new_row = Vec::new();
        new_row.resize(max_x + 1, false);

        grid.push(new_row);
    }

    for (col, row) in points {
        grid[row][col] = true;
    }

    // and now for instructions

    let instructions = bottom
        .lines()
        .map(|l| {
            l.split(" ").collect_vec()[2]
                .split("=")
                .collect_tuple()
                .unwrap()
        })
        .map(|(d, n)| Instruction {
            num: n.parse().unwrap(),
            along_x: d == "x",
        })
        .collect_vec();

    (grid, instructions)
}

fn print_grid(g: &GRID) {
    let mut lines = String::new();
    for r in g {
        lines.push_str(&r.iter().map(|&b| if b { '#' } else { '.' }).join(""));
        lines.push('\n');
    }

    lines.push('\n');
    println!("{}", lines)
}

fn fold(g: GRID, instruction: &Instruction) -> GRID {
    if instruction.along_x {
        let left = g
            .iter()
            .map(|r| (&r[(instruction.num + 1)..]).to_vec())
            .collect_vec();
        let right = g
            .iter()
            .map(|r| {
                let mut v = (&r[..instruction.num]).to_vec();
                v.reverse();
                v
            })
            .collect_vec();

        right
            .iter()
            .zip(left)
            .map(|(x, y)| x.iter().zip(y).map(|(&x, y)| x || y).collect_vec())
            .collect_vec()
    } else {
        let top = g[..instruction.num].to_vec();
        let mut bottom = g[(instruction.num + 1)..].to_vec();

        bottom.reverse();
        top.iter()
            .zip(&bottom)
            .map(|(x, y)| x.iter().zip(y).map(|(&a, &b)| a || b).collect_vec())
            .collect_vec()
    }
}

pub fn part_1(input: &String) -> usize {
    // let input = &TEST_INPUT.to_owned();
    let (g, instructions) = parse_input(input);
    let g = fold(g, &instructions[0]);
    g.iter().flatten().filter(|&&x| x).count()
}

pub fn part_2(input: &String) -> usize {
    let (mut g, instructions) = parse_input(input);

    for i in &instructions {
        g = fold(g.clone(), i);
    }

    // No I dont know why its reversed
    g = g
        .iter()
        .map(|x| ((*x).clone()).into_iter().rev().collect_vec())
        .collect_vec();

    print_grid(&g);

    0
}
