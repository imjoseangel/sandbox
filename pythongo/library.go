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

func main() {

}
