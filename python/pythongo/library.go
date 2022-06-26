package main

import (
	"C"
	"encoding/json"
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

//export fromJSON
func fromJSON(documentPtr *C.char) {
	documentString := C.GoString(documentPtr)
	var jsonDocument map[string]interface{}
	err := json.Unmarshal([]byte(documentString), &jsonDocument)
	if err != nil {
		log.Fatal(err)
	}
	log.Println(jsonDocument)
}

func main() {

}
