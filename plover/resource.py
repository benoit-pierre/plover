
import io
import os.path
import pkg_resources
from contextlib import contextmanager

from plover.registry import registry, ASSET_SCHEME


def resource_exists(resource_name):
    if resource_name.startswith(ASSET_SCHEME):
        assets = registry.get_assets()
        return resource_name in assets
    return os.path.exists(resource_name)

def resource_filename(resource_name):
    if resource_name.startswith(ASSET_SCHEME):
        assets = registry.get_assets()
        return pkg_resources.resource_filename(*assets[resource_name])
    return resource_name

def resource_stream(resource_name, encoding=None):
    filename = resource_filename(resource_name)
    mode = 'rb' if encoding is None else 'r'
    return io.open(filename, mode, encoding=encoding)

def resource_string(resource_name, encoding=None):
    if resource_name.startswith(ASSET_SCHEME):
        assets = registry.get_assets()
        s = pkg_resources.resource_string(*assets[resource_name])
        return s if encoding is None else unicode(s, encoding)
    mode = 'rb' if encoding is None else 'r'
    with io.open(resource_name, mode, encoding=encoding) as fp:
        return fp.read()

