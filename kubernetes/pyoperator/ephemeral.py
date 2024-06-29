import os
from typing import Mapping, Any
import kopf
import kubernetes
import yaml


@kopf.on.create('ephemeralvolumeclaims')
def create_fn(spec, name, namespace, logger, body, **kwargs):

    size = spec.get('size')
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    path = os.path.join(os.path.dirname(__file__), 'pvc.yaml')
    tmpl = open(path, 'rt').read()
    text = tmpl.format(name=name, size=size)
    data = yaml.safe_load(text)

    kopf.adopt(data)

    api = kubernetes.client.CoreV1Api()
    obj = api.create_namespaced_persistent_volume_claim(
        namespace=namespace,
        body=data,
    )

    logger.info(f"PVC child is created: {obj}")

    return {'pvc-name': obj.metadata.name}


@kopf.on.update('ephemeralvolumeclaims')
def update_fn(spec, status, namespace, logger, **kwargs):

    size = spec.get('size', None)
    if not size:
        raise kopf.PermanentError(f"Size must be set. Got {size!r}.")

    pvc_name = status['create_fn']['pvc-name']
    pvc_patch = {'spec': {'resources': {'requests': {'storage': size}}}}

    api = kubernetes.client.CoreV1Api()
    obj = api.patch_namespaced_persistent_volume_claim(
        namespace=namespace,
        name=pvc_name,
        body=pvc_patch,
    )

    logger.info(f"PVC child is updated: {obj}")


@kopf.on.field('ephemeralvolumeclaims', field='metadata.labels')
def propagate_labels(labels: Mapping[str, str], name: str, namespace: str, **_: Any):

    # TODO: use diff-DSL to flat-walk over labels (including deletions, incl. new [labels] section).
    pvc_patch = {'metadata': {'labels': dict(labels)}}

    api = kubernetes.client.CoreV1Api()
    api.patch_namespaced_persistent_volume_claim(
        namespace=namespace,
        name=name,
        body=pvc_patch,
    )
