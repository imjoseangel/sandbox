package main

import (
	"fmt"
	"math"
)

type ErrNegativeSqrt float64

func (e ErrNegativeSqrt) Error() string {
	return fmt.Sprintf("cannot Sqrt negative number: %v", float64(e))
}

func Sqrt(x float64) (float64, error) {
	if x < 0 {
		return math.NaN(), ErrNegativeSqrt(x)
	}

	z := float64(1)
	for i := 0; i < 100; i++ {
		z = z - (z*z-x)/(2*z)
		if math.Abs(z*z-x) < 1e-12 {
			break
		}
	}
	return z, nil
}

func main() {
	for _, number := range []float64{2, -2} {
		result, err:= Sqrt(number)
		if err != nil {
			fmt.Println(err)
		} else {
			fmt.Println(result)
		}
	}
}
