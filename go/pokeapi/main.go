package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

func main() {
	response, err := http.Get("https://pokeapi.co/api/v2/pokemon/ditto")

	if err != nil {
		fmt.Print(err.Error())
		os.Exit(1)
	}

	responseData, err := io.ReadAll(response.Body)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(responseData))
}
