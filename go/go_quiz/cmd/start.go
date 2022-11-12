package cmd

import (
	"fmt"

	"github.com/imjoseangel/sandbox/go/go_quiz/pkg"
	"github.com/spf13/cobra"
)

var startCmd = &cobra.Command{
	Use:   "start",
	Short: "Starting a new Quiz",
	Run: func(cmd *cobra.Command, args []string) {
		res, err := pkg.Quiz()
		if err != nil {
			fmt.Println(err)
			fmt.Printf("Your Score is %d", res)
		} else {
			if res == 16 {
				fmt.Println("Congrats!, you got all questions Correct")
			}
			fmt.Printf("Your Score is %d", res)
		}
	},
}

func init() {
	rootCmd.AddCommand(startCmd)
}
