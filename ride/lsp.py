import sublime

import tempfile

from .settings import ride_settings
from .rcommand import R
from .utils import is_package, is_supported_file


UNLOAD_MESSAGE = """
R-IDE: LSP is not installed. Please install it via Package Control.
"""

try:
    from LSP.plugin.core.handlers import LanguageHandler
    from LSP.plugin.core.settings import ClientConfig
    LSP_FOUND = True
except Exception:
    print(UNLOAD_MESSAGE)
    LSP_FOUND = False


if LSP_FOUND:

    class LspRLangPlugin(LanguageHandler):
        @property
        def name(self):
            return "rlang"

        def __init__(self):
            self._config = ClientConfig(
                name=self.name,
                binary_args=[
                    ride_settings.r_binary(),
                    "--quiet",
                    "--slave",
                    "-e",
                    "languageserver::run()"
                ],
                tcp_port=None,
                scopes=["source.r", "text.html.markdown.rmarkdown"],
                syntaxes=[
                    "Packages/R/R.sublime-syntax",
                    "Packages/R-IDE/R Markdown.sublime-syntax"
                ],
                languageId='r',
                languages=[],
                enabled=False,
                init_options=dict(),
                settings={
                    "diagnostics": ride_settings.get("diagnostics", True),
                    "debug": ride_settings.get("lsp_debug", False)
                },
                env={
                    "PATH": ride_settings.custom_env("PATH"),
                    "LANG": ride_settings.custom_env("LANG")
                }
            )

        @property
        def config(self):
            return self._config

        def on_start(self, window):
            return is_package(window) or is_supported_file(window.active_view())

    class LspCqueryRPlugin(LanguageHandler):
        @property
        def name(self):
            return "cquery-r"

        def __init__(self):
            self._config = ClientConfig(
                name=self.name,
                binary_args=[
                    "cquery"
                ],
                tcp_port=None,
                scopes=[
                    "source.c",
                    "source.c++",
                    "source.c++.rcpp"
                ],
                syntaxes=[
                    "Packages/C++/C.sublime-syntax",
                    "Packages/C++/C++.sublime-syntax",
                    "Packages/R-IDE/Rcpp.sublime-syntax"
                ],
                languageId='c++',
                languages=[],
                enabled=False,
                init_options={
                    "cacheDirectory": tempfile.mkdtemp(),
                    "extraClangArguments": [
                        "-I{}".format(R(script="cat(R.home('include'))"))
                    ],
                    "completion": {
                        "enableSnippets": False
                    }
                },
                settings=dict()
            )

        @property
        def config(self):
            return self._config

        def on_start(self, window):
            return is_package(window) or is_supported_file(window.active_view())

    def plugin_loaded():
        pass

else:
    class LspRLangPlugin():
        pass

    class LspCqueryRPlugin():
        pass

    def plugin_loaded():
        sublime.message_dialog(UNLOAD_MESSAGE)
