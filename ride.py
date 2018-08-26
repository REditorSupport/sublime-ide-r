from .ride import *


def plugin_loaded():
    lsp_plugin_loaded()


def plugin_unloaded():
    main_menu_plugin_unloaded()
