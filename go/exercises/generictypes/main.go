package main

import "fmt"

// List represents a singly-linked list that holds
// values of any type.
type List[T any] struct {
	next *List[T]
	val  T
}

func main() {

	var l1 List[string]
	l1 = List[string]{val: "hello", next: &List[string]{val: "world", next: nil}}

	fmt.Println(l1.val, l1.next.val)

}
