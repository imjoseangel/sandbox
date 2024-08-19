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

		fmt.Println(math.Abs(z - result))
		if math.Abs(result-z) < 1e-6 {
			break
		}
		result = z
	}
	return z
}

func main() {
	manual := Sqrt(2)
	module := math.Sqrt(2)
	fmt.Printf("Guess: %v, Expected: %v, Error: %v",
		manual, module, math.Abs(manual-module))
}
