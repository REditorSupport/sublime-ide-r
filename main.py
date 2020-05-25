from .ride.commands import (
    RideSourcePromptCommand,
    RideExtractFunctionCommand
)

from .ride.buildsys import (
    RideExecCommand, RideExecCoreCommand,
    plugin_unloaded as build_plugin_unloaded,
    RideDynamicMenuListener, RideDynamicBuildListener
)

from .ride.lsp import (
    LspRLangPlugin,
    plugin_loaded as lsp_plugin_loaded
)


def plugin_loaded():
    lsp_plugin_loaded()


def plugin_unloaded():
    build_plugin_unloaded()
