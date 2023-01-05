package main

import "fmt"

func main() {
	x := 5
	p := &x

	fmt.Println(p)  // prints the memory address of x
	fmt.Println(*p) // prints the value stored at the memory address of x (i.e. 5)
}
