from .ride.generate import (
    plugin_loaded as generate_plugin_loaded,
    plugin_unloaded as generate_plugin_unloaded,
    RideMenuListener, RideRegenerateBuildCommand
)
from .ride.source_prompt import RideSourcePromptCommand
from .ride.extract_function import RideExtractFunctionCommand
from .ride.exec import RideExecCommand, RideExecCoreCommand
from .ride.lsp import (
    LspRLangPlugin, LspCqueryRPlugin,
    plugin_loaded as lsp_plugin_loaded
)


def plugin_loaded():
    generate_plugin_loaded()
    lsp_plugin_loaded()


def plugin_unloaded():
    generate_plugin_unloaded()
