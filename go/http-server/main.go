package main

import (
	"fmt"
	"net/http"
)

func main() {
	addr := ":8080" // Specify the port to listen on

	// Create a new multiplexer (router)
	mux := http.NewServeMux()

	// Define routes
	mux.HandleFunc("/", handleRoot)
	mux.HandleFunc("/hello", handleHello)

	// Create a new HTTP server
	server := &http.Server{
		Addr:    addr,
		Handler: mux,
	}

	// Start the server
	fmt.Printf("Server listening on %s\n", addr)
	if err := server.ListenAndServe(); err != nil {
		fmt.Printf("Error starting server: %s\n", err)
	}
}

func handleRoot(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Welcome to the homepage!")
}

func handleHello(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, World!")
}
