package main

import "fmt"

type Sugar struct {
	previous *Sugar
	Location string
}

func main() {
	sugar := Sugar{
		Location: "Coslada",
	}

	sugar1 := Sugar{
		previous: &sugar,
		Location: "Mejorada",
	}

	sugar2 := Sugar{
		previous: &sugar1,
		Location: "Cabanillas",
	}

	fmt.Println("Current location:", sugar2.Location)
	fmt.Println("Previous location:", sugar2.previous.Location)
	fmt.Println("Previous previous location:", sugar2.previous.previous.Location)

}
