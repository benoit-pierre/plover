
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
        self._scripts = {}
        self._systems = {}
        self._machines = {}
        self._dictionaries = {}

    def load_plugins(self, plugins_dir=None):
        if plugins_dir is None:
            plugins_dir = PLUGINS_DIR
        log.info('loading plugins from %s', plugins_dir)
        working_set = pkg_resources.working_set
        environment = pkg_resources.Environment([plugins_dir])
        distributions, errors = working_set.find_plugins(environment)
        for dist in distributions:
            if dist.location.startswith(plugins_dir):
                log.info('plugin: %s [%s]',
                         dist.project_name,
                         dist.version)
        map(working_set.add, distributions)
        if errors:
            log.error("error(s) while loading plugins: %s", errors)

    def _add_entrypoint(self, plugin_type, plugin_dict, entrypoint):
        if entrypoint.name in plugin_dict:
            if entrypoint != plugin_dict[entrypoint.name]:
                log.warning('ignoring duplicate %s: %s [%s]',
                            plugin_type, entrypoint.name,
                            entrypoint.dist.project_name)
            return
        log.info('%s: %s [%s]',
                 plugin_type, entrypoint.name,
                 entrypoint.dist.project_name)
        plugin_dict[entrypoint.name] = entrypoint

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
                        log.info('%s %s [%s]', ASSET_SCHEME, resource_id,
                                 entrypoint.dist.project_name)
                except Exception:
                    log.error('loading entrypoint %s: %s [%s]',
                              assets_type, entrypoint.name,
                              entrypoint.dist.project_name,
                              exc_info=True)
        for plugin_dict, plugin_type in (
            (self._systems, 'system'),
            (self._machines, 'machine'),
            (self._dictionaries, 'dictionary'),
        ):
            entrypoint_type = 'plover.%s' % plugin_type
            for entrypoint in pkg_resources.iter_entry_points(entrypoint_type):
                self._add_entrypoint(plugin_type, plugin_dict, entrypoint)

        for entrypoint in pkg_resources.iter_entry_points('console_scripts'):
            self._add_entrypoint('script', self._scripts, entrypoint)

    def get_assets(self):
        return self._assets

    def get_scripts(self):
        return self._scripts

    def get_systems(self):
        return self._systems

    def get_machines(self):
        return self._machines

    def get_dictionaries(self):
        return self._dictionaries


registry = Registry()

