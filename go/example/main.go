package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {
	// Create a new HTTP request
	req, err := http.NewRequest("GET", "https://example.com", nil)
	if err != nil {
		fmt.Println(err)
		return
	}

	// Send the request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer resp.Body.Close()

	// Read the response body
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
		return
	}

	fmt.Println(string(body))
}
