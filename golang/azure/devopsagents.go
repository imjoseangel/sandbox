///bin/true; exec /usr/bin/env go run "" "$@"
package main

import (
	"encoding/base64"
	"io/ioutil"
	"log"
	"net/http"
	"os"
)

var (
	auth         string
	encodeauth   string
	headers      map[string]string
	secret       string
	organization string
	poolid       string
)

// "github.com/Azure/go-autorest/autorest/azure/auth"

func authencode() string {

	token, tokenpresent := os.LookupEnv("ADV_TOKEN")

	if tokenpresent {
		auth = ":" + token
		encodeauth = base64.StdEncoding.EncodeToString([]byte(auth))
	}
	return encodeauth

}

func get_running() {

	encodeauth = authencode()

	org, _ := os.LookupEnv("ADV_ORG")
	pool, _ := os.LookupEnv("ADV_POOL")

	url := "https://dev.azure.com/" + org + "/_apis/distributedtask/pools/" + pool + "/jobrequests"

	request, _ := http.NewRequest("GET", url, nil)
	request.Header.Add("Authorization", "Basic "+encodeauth)

	client := &http.Client{}
	response, err := client.Do(request)

	if err != nil {
		log.Println("Error on response.\n[ERROR] -", err)
	}
	defer response.Body.Close()

	body, err := ioutil.ReadAll(response.Body)

	if err != nil {
		log.Println("Error while reading the response bytes:", err)
	}

	log.Println(string([]byte(body)))
}

func main() {

	get_running()

}
