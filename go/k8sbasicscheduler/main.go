package main

import (
	"fmt"

	v1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/fields"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/cache"
)

func main() {
	// configure kubernetes client
	config, err := rest.InClusterConfig()
	if err != nil {
		panic(err.Error())
	}

	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		panic(err.Error())
	}

	// watch for unschedulable pods
	watchlist := cache.NewListWatchFromClient(clientset.CoreV1().RESTClient(), "pods",
		v1.NamespaceAll, fields.OneTermEqualSelector("spec.schedulerName", "my-scheduler"))

	_, controller := cache.NewInformer(watchlist, &v1.Pod{}, 0, cache.ResourceEventHandlerFuncs{
		AddFunc: func(obj interface{}) {
			pod := obj.(*v1.Pod)
			fmt.Printf("New unschedulable pod: %s/%s\n", pod.Namespace, pod.Name)
			// Implement your logic here
		},
	})
	// Start the custom scheduler
	stop := make(chan struct{})
	defer close(stop)
	go controller.Run(stop)

	// Keep the process running
	select {}
}
