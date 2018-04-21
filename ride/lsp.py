from .settings import ride_settings
try:
    from LSP.plugin.core.handlers import LanguageHandler
    from LSP.plugin.core.settings import ClientConfig
    LSP_FOUND = True
except Exception:
    print("LSP not found.")
    LSP_FOUND = False


if LSP_FOUND:
    class LspRLangPlugin(LanguageHandler):
        name = "rlang"

        def __init__(self):
            r_binary = ride_settings.get("r_binary", "R")
            if not r_binary:
                r_binary = "R"

            self._config = ClientConfig(
                name=self.name,
                binary_args=[
                    r_binary,
                    "--quiet",
                    "--slave",
                    "-e",
                    "languageserver::run()"
                ],
                tcp_port=None,
                scopes=["source.r"],
                syntaxes=[
                    "Packages/R/R.sublime-syntax",
                    "Packages/RIDE/R Markdown.sublime-syntax"
                ],
                languageId='r',
                enabled=True,
                init_options=dict(),
                settings=dict(),
                env=dict()
            )

        @property
        def config(self):
            return self._config

        def on_start(self, window):
            return True
