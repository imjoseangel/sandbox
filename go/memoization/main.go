package main

import (
	"fmt"
	"time"
)

var memoF = Memo(func(a int) string {
	// expensive computation:
	time.Sleep(time.Millisecond * time.Duration(a))
	return fmt.Sprint(a)
})

r := memoF(2) // the first call is slow
r = memoF(2) // other calls are fast

fmt.Println(r)
// Output: 2
