package main

import "golang.org/x/tour/pic"

func Pic(dx, dy int) [][]uint8 {
	slide := make([][]uint8, dy)

	for i := 0; i < dy; i++ {
		slide[i] = make([]uint8, dx)
		for j := 0; j < dx; j++ {
			slide[i][j] = uint8(i ^ j)
		}
	}

	return slide
}

func main() {
	pic.Show(Pic)
}
