use colored::Colorize;
use std::fmt;

pub const ALL_CORNERS: [[u8; 3]; 24] = [
    [0, 2, 1],
    [1, 0, 2],
    [2, 1, 0],
    [0, 1, 5],
    [5, 0, 1],
    [1, 5, 0],
    [5, 1, 3],
    [3, 5, 1],
    [1, 3, 5],
    [3, 1, 2],
    [2, 3, 1],
    [1, 2, 3],
    [0, 4, 2],
    [2, 0, 4],
    [4, 2, 0],
    [2, 4, 3],
    [3, 2, 4],
    [4, 3, 2],
    [3, 4, 5],
    [5, 3, 4],
    [4, 5, 3],
    [5, 4, 0],
    [0, 5, 4],
    [4, 0, 5],
];

#[derive(Debug)]
pub struct Cube<const N: usize> {
    colors: [[[u8; N]; N]; 6],
}

impl<const N: usize> Cube<N> {
    pub fn solved() -> Cube<N> {
        let mut cube: Cube<N> = Cube::<N> {
            colors: [[[0; N]; N]; 6],
        };
        for (i, face) in cube.colors.iter_mut().enumerate() {
            for row in face.iter_mut() {
                for cell in row.iter_mut() {
                    *cell = i as u8;
                }
            }
        }
        cube
    }
    pub fn turn_slice(&mut self, axis: usize, slice: usize, rotations: usize) {
        if axis > 2 {
            panic!("axis must be 0, 1 or 2");
        }
        if slice >= N {
            panic!(
                "slice can't be greater or equal to n, slice: {}, n: {}",
                slice, N
            );
        }
        if rotations == 0 || rotations > 3 {
            panic!("rotations must be 1, 2 or 3");
        }

        for _ in 0..rotations {
            if slice == 0 || slice == N - 1 {
                let face = if slice == 0 { axis } else { axis + 3 };
                let old = self.colors[face];
                for (y, row) in self.colors[face].iter_mut().enumerate() {
                    for (x, cell) in row.iter_mut().enumerate() {
                        *cell = old[N - 1 - x][y];
                    }
                }
            }

            let axis1 = (axis + 1) % 3;
            let axis2 = (axis + 2) % 3;
            for y in 0..N {
                let temp = self.colors[axis1][y][slice];
                self.colors[axis1][y][slice] = self.colors[axis2][slice][N - y - 1];
                self.colors[axis2][slice][N - y - 1] = self.colors[axis1 + 3][N - y - 1][slice];
                self.colors[axis1 + 3][N - y - 1][slice] = self.colors[axis2 + 3][slice][y];
                self.colors[axis2 + 3][slice][y] = temp;
            }
        }
    }

    pub fn get_corner(&self, colors: [u8; 3]) -> [usize; 3] {
        for face in 0..3 {
            if self.colors[face][0][0] == colors[0]
                && self.colors[(face + 2) % 3][0][0] == colors[1]
                && self.colors[(face + 1) % 3][0][0] == colors[2]
            {
                return [face, (face + 2) % 3, (face + 1) % 3];
            }
            if self.colors[face][0][N - 1] == colors[0]
                && self.colors[(face + 1) % 3][N - 1][0] == colors[1]
                && self.colors[((face + 2) % 3) + 3][0][0] == colors[2]
            {
                return [face, (face + 1) % 3, ((face + 2) % 3) + 3];
            }
            if self.colors[face][N - 1][0] == colors[0]
                && self.colors[((face + 1) % 3) + 3][0][0] == colors[1]
                && self.colors[(face + 2) % 3][0][N - 1] == colors[2]
            {
                return [face, ((face + 1) % 3) + 3, (face + 2) % 3];
            }
            if self.colors[face][N - 1][N - 1] == colors[0]
                && self.colors[((face + 2) % 3) + 3][0][N - 1] == colors[1]
                && self.colors[((face + 1) % 3) + 3][N - 1][0] == colors[2]
            {
                return [face, ((face + 2) % 3) + 3, ((face + 1) % 3) + 3];
            }
        }
        for face in 3..6 {
            if self.colors[face][0][0] == colors[0]
                && self.colors[(face + 1) % 3][0][N - 1] == colors[1]
                && self.colors[(face + 2) % 3][N - 1][0] == colors[2]
            {
                return [face, (face + 1) % 3, (face + 2) % 3];
            }
            if self.colors[face][0][N - 1] == colors[0]
                && self.colors[((face + 2) % 3) + 3][N - 1][0] == colors[1]
                && self.colors[(face + 1) % 3][N - 1][N - 1] == colors[2]
            {
                return [face, ((face + 2) % 3) + 3, (face + 1) % 3];
            }
            if self.colors[face][N - 1][0] == colors[0]
                && self.colors[(face + 2) % 3][N - 1][N - 1] == colors[1]
                && self.colors[((face + 1) % 3) + 3][0][N - 1] == colors[2]
            {
                return [face, (face + 2) % 3, ((face + 1) % 3) + 3];
            }
            if self.colors[face][N - 1][N - 1] == colors[0]
                && self.colors[((face + 1) % 3) + 3][N - 1][N - 1] == colors[1]
                && self.colors[((face + 2) % 3) + 3][N - 1][N - 1] == colors[2]
            {
                return [face, ((face + 1) % 3) + 3, ((face + 2) % 3) + 3];
            }
        }

        panic!("corner not found: {:?}", colors);
    }

    pub fn to_string(&self) -> String {
        let green_face = self.colors[0];

        let mut blue_face = [[0u8; N]; N];
        for (y, row) in self.colors[3].iter().enumerate() {
            for (x, cell) in row.iter().enumerate() {
                blue_face[y][N - x - 1] = *cell;
            }
        }

        let mut white_face = [[0u8; N]; N];
        for (y, row) in self.colors[1].iter().enumerate() {
            for (x, cell) in row.iter().enumerate() {
                white_face[N - x - 1][y] = *cell;
            }
        }

        let mut yellow_face = [[0u8; N]; N];
        for (y, row) in self.colors[4].iter().enumerate() {
            for (x, cell) in row.iter().enumerate() {
                yellow_face[x][y] = *cell;
            }
        }

        let mut orange_face = [[0u8; N]; N];
        for (y, row) in self.colors[2].iter().enumerate() {
            for (x, cell) in row.iter().enumerate() {
                orange_face[x][N - y - 1] = *cell;
            }
        }

        let mut red_face = [[0u8; N]; N];
        for (y, row) in self.colors[5].iter().enumerate() {
            for (x, cell) in row.iter().enumerate() {
                red_face[x][y] = *cell;
            }
        }

        let mut cube_str = String::new();

        for row in white_face.iter() {
            for _ in 0..N * 2 + 1 {
                cube_str.push(' ');
            }
            cube_str.push_str(&row_to_string(row));
            cube_str.push('\n');
        }

        cube_str.push('\n');

        for y in 0..N {
            cube_str.push_str(&row_to_string(&orange_face[y]));
            cube_str.push(' ');
            cube_str.push_str(&row_to_string(&green_face[y]));
            cube_str.push(' ');
            cube_str.push_str(&row_to_string(&red_face[y]));
            cube_str.push(' ');
            cube_str.push_str(&row_to_string(&blue_face[y]));
            cube_str.push('\n');
        }

        cube_str.push('\n');

        for row in yellow_face.iter() {
            for _ in 0..N * 2 + 1 {
                cube_str.push(' ');
            }
            cube_str.push_str(&row_to_string(row));
            cube_str.push('\n');
        }

        cube_str
    }
}

fn row_to_string<const N: usize>(row: &[u8; N]) -> String {
    let mut row_str = String::new();
    for cell in row.iter() {
        row_str.push_str(
            &match cell {
                0 => "  ".on_truecolor(0, 255, 0),
                1 => "  ".on_truecolor(255, 255, 255),
                2 => "  ".on_truecolor(255, 165, 0),
                3 => "  ".on_truecolor(0, 0, 255),
                4 => "  ".on_truecolor(255, 255, 0),
                5 => "  ".on_truecolor(255, 0, 0),

                _ => "  ".on_truecolor(0, 0, 0),
            }
            .to_string(),
        )
    }
    row_str
}

impl<const N: usize> fmt::Display for Cube<N> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.to_string())
    }
}

#[cfg(test)]
mod tests {
    use crate::cube;

    #[test]
    fn get_corner() {
        let c = cube::Cube::<2>::solved();
        for corner in cube::ALL_CORNERS {
            let pos = c.get_corner(corner);
            assert_eq!(corner, [pos[0] as u8, pos[1] as u8, pos[2] as u8]);
        }
    }
}
