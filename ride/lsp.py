import sublime


from .settings import ride_settings
from .utils import selector_is_active


UNLOAD_MESSAGE = """
R-IDE: LSP is not installed. Please install it via Package Control.
"""

try:
    import LSP  # noqa
    LSP_FOUND = True
except Exception:
    print(UNLOAD_MESSAGE)
    LSP_FOUND = False


if LSP_FOUND and sublime.version() > "4000":
    from LSP.plugin.core.sessions import AbstractPlugin

    class LspRLangPlugin(AbstractPlugin):
        @classmethod
        def name(cls):
            return "rlang"

        @classmethod
        def configuration(cls):
            basename = "LSP-rlang.sublime-settings"
            filepath = "Packages/R-IDE/{}".format(basename)
            return sublime.load_settings(basename), filepath

    def plugin_loaded():
        pass

elif LSP_FOUND:
    from LSP.plugin.core.handlers import LanguageHandler
    from LSP.plugin.core.settings import ClientConfig

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

    def plugin_loaded():
        pass


else:
    class LspRLangPlugin():
        pass

    def plugin_loaded():
        sublime.message_dialog(UNLOAD_MESSAGE)
