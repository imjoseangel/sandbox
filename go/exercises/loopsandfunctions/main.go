package main

import (
	"fmt"
	"math"
)

func Sqrt(x float64) float64 {
	if x < 0 {
		return math.NaN()
	}

	z := float64(1)
	for i := 0; i < 100; i++ {
		z = z - (z*z-x)/(2*z)
		if math.Abs(z*z-x) < 1e-12 {
			break
		}
	}
	return z
}

func main() {
	manual := Sqrt(2)
	module := math.Sqrt(2)
	fmt.Printf("Guess: %v, Expected: %v, Error: %v",
		manual, module, math.Abs(manual-module))
}
