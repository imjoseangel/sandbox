package main

import "fmt"

func main() {
	// Print a prompt to the user
	fmt.Print("Enter a number: ")

	// Declare a variable to store the user input
	var num int

	// Read a single number from the standard input and store it in the num variable
	fmt.Scanf("%d", &num)

	// Print the number back to the user
	fmt.Println("You entered: ", num)
}
