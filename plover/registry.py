
import pkg_resources
import glob
import sys
import os

from plover.oslayer.config import CONFIG_DIR
from plover import log


ASSET_SCHEME = 'asset:'
PLUGINS_DIR = os.path.join(CONFIG_DIR, 'plugins')


class Registry(object):

    def __init__(self):
        self._assets = {}
        self._systems = {}
        self._machines = {}

    def load_plugins(self, plugins_dir=PLUGINS_DIR):
        log.info('loading plugins from %s', plugins_dir)
        working_set = pkg_resources.working_set
        environment = pkg_resources.Environment([plugins_dir])
        distributions, errors = working_set.find_plugins(environment)
        map(working_set.add, distributions)
        if errors:
            log.error("error(s) while loading plugins: %s", errors)

    def update(self):
        for assets_type, entrypoint_name in (
            ('dictionary', 'dictionaries'),
            ('wordlist', 'wordlists'),
        ):
            for entrypoint in pkg_resources.iter_entry_points('plover.asset',
                                                              name=entrypoint_name):
                try:
                    for name, resource_name in entrypoint.load():
                        resource_id = '%s%s:%s' % (
                            ASSET_SCHEME,
                            assets_type,
                            name,
                        )
                        self._assets[resource_id] = (entrypoint.module_name,
                                                     resource_name)
                        log.info('%s %s', ASSET_SCHEME, resource_id)
                except Exception:
                    log.error('loading entrypoint %s: %s (from %s)',
                              assets_type, entrypoint.name,
                              entrypoint.module_name,
                              exc_info=True)
        for plugin_dict, plugin_type in (
            (self._systems, 'system'),
            (self._machines, 'machine'),
        ):
            entrypoint_type = 'plover.%s' % plugin_type
            for entrypoint in pkg_resources.iter_entry_points(entrypoint_type):
                if entrypoint.name in plugin_dict:
                    if entrypoint != plugin_dict[entrypoint.name]:
                        log.warning('ignoring duplicate %s: %s (from %s)',
                                    plugin_type,
                                    entrypoint.name,
                                    entrypoint.module_name)
                    continue
                log.info('%s: %s (from %s)',
                         plugin_type, entrypoint.name,
                         entrypoint.module_name)
                plugin_dict[entrypoint.name] = entrypoint

    def get_assets(self):
        return self._assets

    def get_systems(self):
        return self._systems

    def get_machines(self):
        return self._machines


registry = Registry()

