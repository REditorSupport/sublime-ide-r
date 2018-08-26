import tempfile

from .settings import ride_settings
from .rcommand import R


UNLOAD_MESSAGE = """
LSP cannot be found. It usually happens when LSP is not installed or
R-IDE is loaded before LSP. For the latter case, please make sure
LSP is installed to "Installed Packages" as a `sublime-package` file.
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
                enabled=True,
                init_options=dict(),
                settings=dict(),
                env={"PATH": ride_settings.custom_env()["PATH"]}
            )

        @property
        def config(self):
            return self._config

        def on_start(self, window):
            return True

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
                    "source.objc",
                    "source.objc++"
                ],
                syntaxes=[
                    "Packages/C++/C.sublime-syntax",
                    "Packages/C++/C++.sublime-syntax",
                    "Packages/Objective-C/Objective-C.sublime-syntax",
                    "Packages/Objective-C/Objective-C++.sublime-syntax"
                    "Packages/R-IDE/Rcpp.sublime-syntax"
                ],
                languageId='objc++',
                languages=[],
                enabled=True,
                init_options={
                    "cacheDirectory": tempfile.mkdtemp(),
                    "extraClangArguments": [
                        "-I{}".format(R(script="cat(R.home('include'))"))
                    ]
                },
                settings=dict()
            )

        @property
        def config(self):
            return self._config

        def on_start(self, window):
            return True

else:
    class LspRLangPlugin():
        pass

    class LspCqueryRPlugin():
        pass
