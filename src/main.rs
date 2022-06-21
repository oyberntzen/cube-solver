mod cube;

fn main() {
    let c = cube::Cube::<2>::solved();

    for corner in cube::ALL_CORNERS {
        let pos = c.get_corner(corner);
        println!("{:?}: {:?}", corner, pos);
    }

    println!("{}", c);
}
