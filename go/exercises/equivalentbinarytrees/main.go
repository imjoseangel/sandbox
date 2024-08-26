package main

import (
	"sync"

	"golang.org/x/tour/tree"
)

// Walk walks the tree t sending all values
// from the tree to the channel ch.
func Walk(t *tree.Tree, ch chan<- int) {
	var wg sync.WaitGroup

	var walk func(t *tree.Tree)
	walk = func(t *tree.Tree) {
		if t == nil {
			return
		}

		wg.Add(1)
		go func() {
			defer wg.Done()
			walk(t.Left)
		}()

		ch <- t.Value

		wg.Add(1)
		go func() {
			defer wg.Done()
			walk(t.Right)
		}()
	}

	walk(t)

	go func() {
		wg.Wait()
		close(ch)
	}()
}

// Same determines whether the trees
// t1 and t2 contain the same values.
func Same(t1, t2 *tree.Tree) bool {
	ch1 := make(chan int)
	ch2 := make(chan int)
	go Walk(t1, ch1)
	go Walk(t2, ch2)
	for {
		v1, ok1 := <-ch1
		v2, ok2 := <-ch2
		if v1 != v2 || ok1 != ok2 {
			return false
		}
		if !ok1 {
			break
		}
	}
	return true
}

func main() {
	ch := make(chan int)
	go Walk(tree.New(3), ch)

	for v := range ch {
		println(v)
	}
}
