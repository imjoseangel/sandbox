package main

import (
	"C"
	"log"
)

//export helloWorld
func helloWorld() {
	log.Println("Hello World")
}

//export hello
func hello(namePtr *C.char) {
	name := C.GoString(namePtr)
	log.Println("Hello", name)
}

//export farewell
func farewell() *C.char {
	return C.CString("Bye!")
}

func main() {

}
