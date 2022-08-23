# Learn how to Speed Up Kubernetes microservices by debugging DNS network traffic

## Introduction

One of the most common bottlenecks when communicating Kubernetes pods is DNS resolution. Analyzing network traffic within Kubernetes is not trivial.

This article will help you to understand how to analyze and debug HTTP and DNS network traffic in Kubernetes.

With your comments and help, I would like to improve this small article as much as possible to reach every single profile and help any developer, network engineer, or Kubernetes enthusiast.

## What is DNS?

DNS is a protocol that allows a computer to resolve a **Domain Name** like *dev.to* written by a human to an **IP address** so browsers can load Internet resources. DNS is called the phonebook of the Internet.

## How to debug DNS network traffic - Wireshark

There are many tools to analyze network traffic, but needless to say, the most common one is *Wireshark*. It is a powerful tool that allows you to analyze network traffic and extract information from it. We will analyze DNS traffic from our computers and will compare later with the traffic from a pod in a Kubernetes cluster.

## What happens when calling a web page?

To understand what happens with the DNS when requesting a web page, this amazing [diagram](https://dev.to/wassimchegham/ever-wondered-what-happens-when-you-type-in-a-url-in-an-address-bar-in-a-browser-3dob) from @wassimchegham is a good start.

The **DNS request**, the **TCP Connection**, the **HTTP Request** and the **HTTP Response** can be easiliy displayed using different filters and the *Statistics - Flow Chart*:

![Flow Chart](./files/example.com-http.png)

In the next section we will learn how to create it.

## Creating the Wireshark Flow Chart

Install Wireshark on your favourite Operating System (Mac, Windows or Linux) and open it.

The initial screen is like this:

![Wireshark Initial Screen](./files/startup-wireshark.png)

Find what of all the interfaces shown is the one being used more actively:

![Active Interface](./files/wireshark-traffic-initial.png)

Just select it to start capturing traffic.
