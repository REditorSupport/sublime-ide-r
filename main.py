from .ride.generate import (
    plugin_unloaded as generate_plugin_unloaded,
    RideDynamicMenuListener, RideDynamicBuildListener
)
from .ride.source_prompt import RideSourcePromptCommand
from .ride.extract_function import RideExtractFunctionCommand
from .ride.exec import RideExecCommand, RideExecCoreCommand
from .ride.lsp import (
    LspRLangPlugin, LspCqueryRPlugin,
    plugin_loaded as lsp_plugin_loaded
)


def plugin_loaded():
    lsp_plugin_loaded()


def plugin_unloaded():
    generate_plugin_unloaded()
