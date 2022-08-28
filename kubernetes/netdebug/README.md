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

The **DNS request**, the **TCP Connection**, the **HTTP Request** and the **HTTP Response** can be easiliy displayed using different filters and the *Statistics - Flow Graph*:

![Flow Graph](/sandbox/kubernetes/netdebug/files/example.com-http.png)

In the next section we will learn how to create it.

## Creating the Wireshark Flow Graph

Install Wireshark on your favourite Operating System (Mac, Windows or Linux) and open it.

The initial screen should be like:

![Wireshark Initial Screen](/sandbox/kubernetes/netdebug/files/startup-wireshark.png)

### Preparing the filter

Before start capturing traffic, let's find the IP of the domain *www.example.com*.

Open a Terminal or CMD Console and run:

```shell
nslookup www.example.com
```

The answer will looks like:

```shell
Server: 8.8.8.8
Address: 8.8.8.8#53

Non-authoritative answer:
Name: www.example.com
Address: 93.184.216.34
```

The `Server` field indicates the DNS server configured in our environment to which we will request to resolve the name `www.example.com`.

Under `Non-authoritative answer:` we will see the name we just requested and the IP associated to it. In our example `93.184.216.34`.

Under *...using this filter:* option in the main screen, input:

`tcp port http or port 53 or dst host 93.184.216.34`

where `93.184.216.34` is the address resolved with `nslookup`.

### Capturing traffic

Select the interface on which packets need to be captured. This will usually be the interface where the Packet/s column is constantly changing, which would indicate the presence of live traffic).

![Active Interface](/sandbox/kubernetes/netdebug/files/wireshark-traffic-initial.png)

It is time to press the *blue fin* icon to start the traffic capture.

![Capture Traffic](/sandbox/kubernetes/netdebug/files/capture-traffic.png)

### Request the URL

If you are using Linux or Mac, run the following from a Terminal:

```shell
curl http://example.com
```

From Windows, use Powershell and run:

```powershell
Invoke-WebRequest http://www.example.com
```

Stop capturing traffic just pressing the big red button. Your screen should looks like:

![http traffic](/sandbox/kubernetes/netdebug/files/example.com-http-traffic.png)

To get the promised Flow Graph, select the *Statistics* menu and *Flow Graph*

## Undertanding the captured traffic

Looking carefully to the captured traffic, we could find two parts. The DNS (In *cyan*) and the HTTP (in *green*)

The first line (In *cyan*), shows the DNS request from our IP address to the DNS Server (8.8.8.8 in the example).

The second *cyan* line shows the DNS response. Selecting it, we can find the IP Address of the requested domain in the *Packet Details Window*. Under **Domain Name System (Response)** - **Answers** like shown in the image below.

![DNS response](/sandbox/kubernetes/netdebug/files/DNS-example.com-IP.png)

### The 3 Way Handshaking (SYN ACK)

Reflected in the next three lines (in *green*).

Before a client and a server can exchange data (payload), the client and server must established a TCP connection. This is done via the TCP 3 way handshake.

**SYN** - The client sends a SYN (Synchronize) packet to the server.
**SYN ACK**- The server sends a SYN ACK (Synchronize Acknowledge) packet to the client.
**ACK** - The client sends an ACK (Acknowledge) packet to the server.

In the image, we can find it after the DNS request.

![3-way](/sandbox/kubernetes/netdebug/files/example.com-3-way.png)

### The Request and Connection Close (FIN ACK)

After that, we can find the HTTP GET and the ACK from the Server with the HTTP response.

Finally we can find the TCP close requests with FIN ACK Packets to close the connection.

![fin-acl](/sandbox/kubernetes/netdebug/files/example.com-finack.png)

## DNS on Kubernetes

To understand how a *Domain Name* is resolved in a pod, first let's create a single deployment:

```shell
kubectl create deployment nginx --image nginx
```

We can find the pod name

```shell
kubectl get pods
```

```shell
NAME                    READY   STATUS    RESTARTS   AGE
nginx-68f67d74bd-p49bt   1/1     Running   0          89s
```

Remember that the DNS resolution inside a container - like any Linux system - is driven by the `/etc/resolv.conf` config file.

```shell
kubectl exec -it nginx-68f67d74bd-p49bt -- cat /etc/resolv.conf
```

The /etc/resolv.conf file inside the container looks like this by default:

```ini
search default.svc.cluster.local svc.cluster.local cluster.local
nameserver 10.96.0.10
options ndots:5
```

We can find 3 or more search Domains in a Kubernetes configuration. The example above comes from a Minikube Cluster where there are 3 local search domains specified.

Take a look also to the `ndots:5` option. It is important to understand how both `search` and `ndots` settings work together.

To understand both concepts, we can refer to the [resolv.conf(5) Linux man page](https://man7.org/linux/man-pages/man5/resolv.conf.5.html)

The `search` represents the search path for a particular domain. Interestingly dev.to or example.com are not FQDN (fully qualified domain name). A standard convention that most DNS resolvers follow is that if a domain ends with . (representing the root zone), the domain is considered to be FQDN. Some resolvers try to act smart and append the . themselves. So dev.to. is an FQDN but dev.to is not.

One important point from the [resolv.conf(5) Linux man page](https://man7.org/linux/man-pages/man5/resolv.conf.5.html) For environments with multiple subdomains please read options `ndots:n` to avoid unnecessary traffic for the root-dns-servers. Note that this process may be slow and will generate a lot of network traffic if the servers for the listed domains are not local, and that queries will time out if no server is available for one of the domains.

The `ndots` represents the threshold value of the number of dots in a query name to consider it as a "fully qualified" domain name.

If `ndots` is set to **5** like the default in Kubernetes, and the name contains less than 5 dots inside it, the syscall will try to resolve it sequentially going through all local search domains first and - in case none succeed - will resolve it as an absolute name only at last.

For instance, if we request `www.example.com`, the query iterates through all search paths until the answer contains a NOERROR code.

1. `www.example.com.<namespace>.svc.cluster.local`
1. `www.google.com.svc.cluster.local`
1. `www.google.cluster.local`
1. `www.google.com`

It is important to remark that A and AAAA records are requested in parallel. This is because single-request option in /etc/resolv.conf has a default configuration to perform parallel IPv4 and IPv6 lookups. This option can be disabled using the configuration option `single-request` in the `/etc/resolv.conf` configuration file.

```ini
option single-request
```

## Capturing Traffic in a Kubernetes Pod

There are different ways to capture traffic in a Kubernetes Pod. All the examples are based in the latest Kubernetes functionality using [Ephemeral Debug Containers](https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#ephemeral-container)

First of all, let's create a `tcpdump` debug image. Wireshark will use it to display the attached pod traffic. We will use a multi-platform image to be able to run in `linux/amd64` and `linux/arm64`

### The Dockerfile

```dockerfile
ARG build_for=linux/amd64,linux/arm64
FROM alpine:latest as base

LABEL maintainer="<yourusername>"

# Packages to build image requirements
RUN apk add --no-cache \
    tcpdump

ENTRYPOINT [ "tcpdump" ]
CMD [ "-i", "any" ]
```

### The build command

To create a multi-platform image in *dockerhub* let's create a builder instance and use the extended build capabilities with BuildKit.

```shell
docker buildx create --name buildx --driver-opt network=host --use
docker buildx inspect --bootstrap
docker buildx build -t <yourusername>/tcpdump:v1.0.0 --platform linux/amd64 --platform linux/arm64 --file Dockerfile --push .
docker buildx imagetools inspect <yourusername>/tcpdump:v1.0.0
docker buildx rm buildx
```

The last output will show both images with their platforms:

```shell
Name:      docker.io/<yourusername>/tcpdump:v1.0.0
MediaType: application/vnd.docker.distribution.manifest.list.v2+json
Digest:    sha256:9dd8cb1d4b77b7d02d41ff8418cd442c01badfe8ecd0c0a3a58f43f528eba378

Manifests:
  Name:      docker.io/<yourusername>/tcpdump:v1.0.0@sha256:0c341c671566dbc3cdded9da05120bb2216142f46516c14cf3d10b6c38997195
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/amd64

  Name:      docker.io/<yourusername>/tcpdump:v1.0.0@sha256:c6de3ab95521c9e7e07a05d99935d19686b8d6e81ab85ce631312cffe57d2ce3
  MediaType: application/vnd.docker.distribution.manifest.v2+json
  Platform:  linux/arm64
```

### Attaching the ephemeral container to the NGINX Pod

Now that the tcpdump image is prepared, just run:

```shell
kubectl debug --image imjoseangel/tcpdump:v1.0.0 nginx-68f67d74bd-p49bt  -c debugger
```

```shell
kubectl exec nginx-68f67d74bd-p49bt -c debugger -- tcpdump -s 0 -n -w - -U -i any | Wireshark -kni -
```
