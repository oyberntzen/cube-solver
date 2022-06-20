mod cube;

fn main() {
    let mut c = cube::Cube::<3>::solved();

    for corner in cube::ALL_CORNERS {
        let pos = c.get_corner(corner);
        println!("{:?}: {:?}", corner, pos);
    }

    println!("{}", c);
}
