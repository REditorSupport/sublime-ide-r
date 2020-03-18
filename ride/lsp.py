import sublime

import tempfile
import os
import sys
import subprocess


from .settings import ride_settings
from .r import R
from .utils import selector_is_active


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
            path = ride_settings.get("r_binary_lsp", None)
            if not path:
                path = ride_settings.r_binary()
            self._config = ClientConfig(
                name=self.name,
                binary_args=[
                    path,
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
                env=ride_settings.ride_env()
            )

        @property
        def config(self):
            return self._config

        def on_start(self, window):
            return selector_is_active(window=window)

    class LspCclsRPlugin(LanguageHandler):
        @property
        def name(self):
            return "ccls-r"

        def __init__(self):
            clang_extraArgs = [
                "-I{}".format(R(script="cat(R.home('include'))"))
            ]
            if sys.platform == "darwin":
                try:
                    sysrootpath = subprocess.check_output(
                        ["xcrun", "--show-sdk-path"]).decode().strip()
                except Exception:
                    sysrootpath = "/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk"
                if os.path.isdir(sysrootpath):
                    clang_extraArgs.append("-isysroot{}".format(sysrootpath))
                try:
                    resourcedir = subprocess.check_output(
                        ["clang", "--print-resource-dir"]).decode().strip()
                except Exception:
                    resourcedir = "/Library/Developer/CommandLineTools/usr/lib/clang/11.0.0"
                if os.path.isdir(resourcedir):
                    clang_extraArgs.append("-isystem{}/../../../include/c++/v1".format(resourcedir))
                    clang_extraArgs.append("-isystem{}/include".format(resourcedir))
                clang_extraArgs.append("-I/usr/include")
                clang_extraArgs.append("-I/usr/local/include")

            self._config = ClientConfig(
                name=self.name,
                binary_args=[
                    ride_settings.get("ccls", "ccls")
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
                    "cache": {"directory": tempfile.mkdtemp()},
                    "clang": {"extraArgs": clang_extraArgs},
                    "client": {"snippetSupport": False}
                },
                settings=dict()
            )

        @property
        def config(self):
            return self._config

        def on_start(self, window):
            return selector_is_active(window=window)

    def plugin_loaded():
        pass

else:
    class LspRLangPlugin():
        pass

    class LspCclsRPlugin():
        pass

    def plugin_loaded():
        sublime.message_dialog(UNLOAD_MESSAGE)
