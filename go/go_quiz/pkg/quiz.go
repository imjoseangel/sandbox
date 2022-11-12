package pkg

import (
	"encoding/csv"
	"errors"
	"fmt"
	"io"
	"log"
	"os"
	"strconv"
)

func Quiz() (res int, err error) {
	res = 0

	f, err := os.Open("data.csv")
	if err != nil {
		log.Fatal(err)
	}

	defer f.Close()

	csvReader := csv.NewReader(f)
	var ans int
	for {
		rec, err := csvReader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}

		fmt.Print(rec[0] + " : ")

		c, _ := strconv.Atoi(rec[1])

		fmt.Scanf("%d\n", &ans)

		if ans == c {
			res = res + 1
			fmt.Println("correct")
			continue

		} else {
			err = errors.New("incorrect response")

			break
		}

	}
	return res, err
}
