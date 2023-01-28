# Kubernetes Pods Stuck in Terminating: A Resolution Guide

A Pod or even a namespace deletion can take some time to deleted or even become a nightmare with a hanging `Terminating` process.

In this post, we will explain possible causes, tips to delete a namespace or pod and how to proceed when there is a Pod on `Terminating` state.

## Reasons for a terminating state

### The PreStop hook and terminationGracePeriodSeconds

One of the reasons why a Pod can stay in the `Terminating` Phase is due to the `terminationGracePeriodSeconds` configuration and Finalizers associated to it. From the [Kubernetes Documentation](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#hook-handler-execution):

> If a `PreStop` hook hangs during execution, the Pod's phase will be `Terminating` and remain there until the Pod is killed after its `terminationGracePeriodSeconds` expires.

For example. This configuration:

```yaml
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
