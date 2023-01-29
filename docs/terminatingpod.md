# Kubernetes Pods Stuck in Terminating: A Resolution Guide

Do you know why a Pod takes too much time to get deleted or even hangs on `Terminating` state?

This post describes the Pod Lifecycle conditions, reasons of why they could hang on `Terminating` state, and some useful tips to get rid of them.

## Pod Termination

There are multiple reasons why the Kubernetes Scheduler can evict a healthy container. For example, the execution of Pods with higher priority, the drain of a node during a version update, an auto-scaling process, a [resource bin-packing](https://kubernetes.io/docs/concepts/scheduling-eviction/resource-bin-packing/) or a simple `kubectl delete` command.

Kubernetes provides for graceful termination when Pods are no longer needed with [Container Lifecycle Hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks). They are executed by the kubelet on the specific containers when it receives the event.

```mermaid
sequenceDiagram
    autonumber
    Stop Container Event-->>SIGTERM: PreStop Hook
    SIGTERM->>SIGKILL: Termination Grace Period
    Note over Stop Container Event,SIGKILL: Termination Process
```

When kubelet knows that a pod should be terminated, it executes the `preStop` lifecycle hook (if exists). It sends the `SIGTERM` to the main process (pid 1) within each container in the pod and waits for their termination. If the applications inside the containers are properly prepared, they will start a graceful shutdown. The duration should not be more than the specified in the [spec.terminationGracePeriodSeconds](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.21/#podspec-v1-core) which is 30 seconds by default.

If the application hasn't completed the shutdown properly, the Kubelet gives a grace period, until removing the pod IP and killing the container by sending a `SIGKILL`. At this point, the Pod is removed.

## Why a Pod can hang on `Terminating` state

The two most common reasons for a pod hanging during the eviction process are an incorrect `terminationGracePeriodSeconds` value and a `Finalizer` dependency.

### The PreStop hook and terminationGracePeriodSeconds

From the [Kubernetes Documentation](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#hook-handler-execution):

> If a `PreStop` hook hangs during execution, the Pod's phase will be `Terminating` and remain there until the Pod is killed after its `terminationGracePeriodSeconds` expires.

For instance. This configuration:

```yaml
spec:
  terminationGracePeriodSeconds: 3600
  containers:
    - lifecycle:
        preStop:
        exec:
          command:
            - /bin/sh
            - -c
            - sleep 3600
```

Will keep our pod on `Terminating` state for 1 hour.

It is essential to handle the `SIGTERM` correctly and ensure that the application terminates gracefully when the kubelet sends the `SIGTERM` to the container.

### Finalizers

From [Kubernetes documentation](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/):

> Finalizers are namespaced keys that tell Kubernetes to wait until specific conditions are met before it fully deletes resources marked for deletion.

If a pod is stuck on Terminating state check the `metadata/finalizers` of the pod. Normally they are used to prevent accidental deletion of resources.

For instance, this example has a `kubernetes` key as `finalizer` normally used on namespaces.

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  finalizers:
    - kubernetes
spec:
  containers:
    - image: nginx
      name: nginx
```

Deleting the pod will not delete it, just update and will keep on `Terminating` state.
