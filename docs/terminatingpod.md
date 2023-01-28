# Kubernetes Pods Stuck in Terminating: A Resolution Guide

A Pod deletion can take some time to get deleted or even hang on `Terminating`.

In this post, we will explain possible causes and give some useful tips to delete PODS when hanging on `Terminating` state.

## Reasons for a pod on `Terminating` state

Leaving out bugs or node issues, the two most common reasons 

### The PreStop hook and terminationGracePeriodSeconds

One of the reasons why a Pod can stay in the `Terminating` Phase is due to the `terminationGracePeriodSeconds` configuration in a deployment. From the [Kubernetes Documentation](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#hook-handler-execution):

> If a `PreStop` hook hangs during execution, the Pod's phase will be `Terminating` and remain there until the Pod is killed after its `terminationGracePeriodSeconds` expires.

For example. This configuration:

```yaml
spec:
  containers:
    - image: nginx
  name: nginx
  lifecycle:
    preStop:
    exec:
      command:
        - /bin/sh
        - -c
        - sleep 3600
  terminationGracePeriodSeconds: 3600
```

Will keep our pod on `Terminating` state for 1 hour.

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
