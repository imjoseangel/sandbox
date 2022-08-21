# Learn how to Speed Up Kubernetes microservices by debugging DNS network traffic

## Introduction

One of the most common bottlenecks I have found during my latest years administering Kubernetes is probably DNS resolution.

This article will help you to understand how to debug HTTP and DNS network traffic in Kubernetes.

I have always had the feeling of explaining *black magic* to my colleages. With your comments and help, I would like to improve it as much as possible and reach every single profile and help any developer, network engineer, or Kubernetes enthusiast.

## What is DNS?

DNS is a protocol that allows a computer to resolve a **Domain Name** like *dev.to* written by a human to an **IP address** so browsers can load Internet resources. DNS is the phonebook of the Internet.

## How to debug DNS network traffic - Wireshark

There are many tools to analyze network traffic, but needless to say, the most common one is **Wireshark**. It is a powerful tool that allows you to analyze network traffic and extract information from it. We will analyze DNS traffic from our computers and will compare later with the traffic from a pod in a Kubernetes cluster.
