package main

import "fmt"

// List represents a singly-linked list that holds
// values of any type.
type List[T any] struct {
	next *List[T]
	val  T
}

func main() {

	// Directly initialize the List with its desired structure instead of assigning it step by step
	var l1 = &List[string]{val: "hello", next: &List[string]{val: "world", next: nil}}

	fmt.Println(l1.val, l1.next.val)

}
