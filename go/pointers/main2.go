package main

import "fmt"

func increment(p *int) {
	*p++
}

func main() {
	x := 5
	increment(&x)
	fmt.Println(x) // prints 6
}
