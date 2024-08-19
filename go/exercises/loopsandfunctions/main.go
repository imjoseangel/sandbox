package main

import (
	"fmt"
	"math"
)

func Sqrt(x float64) float64 {
	z := float64(1)
	result := float64(1)
	for i := 0; i < 100; i++ {
		z -= (z*z - x) / (2 * z)
		fmt.Println(i)
		fmt.Println(math.Abs(z - result))

		if math.Abs(result-z) < 1e-5 {
			break
		}
		result = z
	}
	return z
}

func main() {
	fmt.Println(Sqrt(10100))
	fmt.Println(math.Sqrt(10100))
}
