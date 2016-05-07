
import os
import sys
import pkg_resources

from utils.metadata import collect_metadata

from PyInstaller import log as logging
from PyInstaller.utils.hooks import eval_statement


log = logging.getLogger(__name__)
log.info('hook-plover.py')

datas = []
hiddenimports = []

distribution = list(pkg_resources.find_distributions('.', only=True))[0]
assert distribution.project_name == 'plover'

metadata = {}
metadata.update(collect_metadata(distribution))

datas.append(('plover/assets', 'plover/assets'))
for group in distribution.get_entry_map().values():
    for entrypoint in group.values():
        hiddenimports.append(entrypoint.module_name)


plugins_dir = os.path.realpath('plugins') + os.path.sep

if os.path.exists(plugins_dir):

    working_set = pkg_resources.working_set
    environment = pkg_resources.Environment([plugins_dir])
    distributions, errors = working_set.find_plugins(environment)
    map(working_set.add, distributions)
    if errors:
        log.error("error(s) while loading plugins: %s", errors)

    plugins_imports = set()

    for distribution in pkg_resources.find_distributions(plugins_dir):
        log.info('adding plugin: %s', distribution.project_name)
        egg = '%s/%s.egg' % (plugins_dir, distribution.egg_name())
        # datas.append((egg, 'eggs'))
        metadata.update(collect_metadata(distribution))
        for group_name, group in distribution.get_entry_map().items():
            for entrypoint in group.values():
                log.info('%s entrypoint: %s [%s]', group_name, entrypoint, entrypoint.module_name)
                script = '''
                plugin_path = %r
                plugins_dir = %r
                import os, sys
                sys.path.insert(0, plugin_path)
                imports = set(sys.modules.keys())
                import %s
                imports = set(sys.modules.keys()) - imports
                hiddenimports = []
                for module_name in imports:
                    if module_name == 'plover' or module_name.startswith('plover.'):
                        continue
                    mod = sys.modules[module_name]
                    if mod is None:
                        continue
                    if not hasattr(mod, '__file__'):
                        # Builtin module
                        continue
                    if not os.path.realpath(mod.__file__).startswith(plugins_dir):
                        hiddenimports.append(module_name)
                print hiddenimports
                ''' % (egg, plugins_dir, entrypoint.module_name)
                result = eval_statement(script)
                plugins_imports.update(result)

    log.info('plugins hidden imports: %s', plugins_imports)
    hiddenimports.extend(plugins_imports)

metadata_list = list(sorted(metadata.items()))
log.info('adding metadata: %s', metadata_list)
datas.extend(metadata_list)

log.info('datas: %s', datas)
log.info('hiddenimports: %s', hiddenimports)

