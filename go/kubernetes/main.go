package main

import (
	"k8s.io/client-go/tools/clientcmd"
)

func main() {

	kubeconfig := "~/.kube/config"

	config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
	if err != nil {
		panic(err.Error())
	}
}
