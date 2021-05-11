///bin/true; exec /usr/bin/env go run "" "$@"
package main

import (
	"encoding/base64"
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

	org, _ := os.LookupEnv("ADV_ORG")
	pool, _ := os.LookupEnv("ADV_POOL")

	url := "https://dev.azure.com/" + org + "/_apis/distributedtask/pools/" + pool + "/jobrequests"

	request, _ := http.NewRequest("GET", url, nil)
	request.Header.Add("Authorization", "Basic "+encodeauth)
}

func main() {

	authencode()

	// authorizer, err := auth.NewAuthorizerFromEnvironment()

}
