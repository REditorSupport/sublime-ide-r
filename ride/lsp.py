import sublime

import tempfile
import os
import sys
import subprocess


from .settings import ride_settings
from .r import R
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
                env=ride_settings.custom_env()
            )

        @property
        def config(self):
            return self._config

        def on_start(self, window):
            return is_package(window) or is_supported_file(window.active_view())

    class LspCclsRPlugin(LanguageHandler):
        @property
        def name(self):
            return "ccls-r"

        def __init__(self):
            clang_extraArgs = [
                "-I{}".format(R(script="cat(R.home('include'))"))
            ]
            if sys.platform == "darwin":
                # https://github.com/MaskRay/ccls/issues/191#issuecomment-453809905
                try:
                    cpath = subprocess.check_output(["clang", "-print-resource-dir"]).decode().strip()
                    cpath = os.path.normpath(os.path.join(cpath, "../../../include/c++/v1"))
                except Exception:
                    cpath = "/Library/Developer/CommandLineTools/usr/include/c++/v1"
                if os.path.isdir(cpath):
                    clang_extraArgs.append("-isystem{}".format(cpath))

                try:
                    sysrootpath = subprocess.check_output(["xcrun", "--show-sdk-path"]).decode().strip()
                except Exception:
                    sysrootpath = "/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk"
                if os.path.isdir(sysrootpath):
                    clang_extraArgs.append("-isysroot{}".format(sysrootpath))

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
            return is_package(window) or is_supported_file(window.active_view())

    def plugin_loaded():
        pass

else:
    class LspRLangPlugin():
        pass

    class LspCclsRPlugin():
        pass

    def plugin_loaded():
        sublime.message_dialog(UNLOAD_MESSAGE)
