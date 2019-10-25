import sublime
import sublime_plugin

from .settings import ride_settings
from .r import R
from .utils import is_package, is_supported_file


class RideExecCommand(sublime_plugin.WindowCommand):
    def run(self, selector="", kill=False, **kwargs):
        if kill:
            self.window.run_command("exec", {"kill": True})
            return

        if "cmd" in kwargs and kwargs["cmd"]:
            self.window.run_command("ride_exec_core", kwargs)
        elif "cmd" not in kwargs:
            sublime.set_timeout(lambda: self.window.run_command(
                    "show_overlay", {
                        "overlay": "command_palette",
                        "command": "ride_exec_core"
                    }), 10)

    def is_enabled(self, selector="", **kwargs):
        scopes = [x.strip() for x in selector.split(",")]
        if "package" in scopes and not is_package(self.window):
            return False

        view = self.window.active_view()
        if "r" in scopes and not is_supported_file(view, "r"):
            return False

        if "rmarkdown" in scopes and not is_supported_file(view, "rmarkdown"):
            return False

        if "rnw" in scopes and not is_supported_file(view, "rnw"):
            return False

        return True


class RideExecCoreCommand(sublime_plugin.WindowCommand):
    def run(self, cmd="", env={}, working_dir="", **kwargs):
        try:
            cmd = "{package}::{function}({args})".format(**kwargs)
        except KeyError:
            pass

        kwargs = {}
        kwargs["cmd"] = [ride_settings.r_binary(), "--quiet", "-e", cmd]
        if not working_dir and is_package(self.window):
            working_dir = self.window.folders()[0]
        kwargs["working_dir"] = working_dir
        _env = ride_settings.custom_env()
        _env.update(env)
        kwargs["env"] = _env
        kwargs = sublime.expand_variables(kwargs, self.window.extract_variables())
        self.window.run_command("exec", kwargs)

    def input(self, *args):
        return RideAskPackage()


class RideAskPackage(sublime_plugin.ListInputHandler):
    packages = []
    _initial_text = None

    def name(self):
        return "package"

    def initial_text(self):
        if RideAskPackage._initial_text:
            return RideAskPackage._initial_text

    def list_items(self):
        if not self.packages:
            self.packages[:] = R(
                "cat(paste(rownames(installed.packages())), sep='\n')").strip().split("\n")
        return self.packages

    def confirm(self, text):
        RideAskPackage._initial_text = text

    def cancel(self):
        RideAskPackage._initial_text = None

    def placeholder(self):
        return "package::"

    def description(self, value, text):
        return "{}::".format(value)

    def next_input(self, args):
        return RideAskFunction(args)


class RideAskFunction(sublime_plugin.ListInputHandler):
    exports = {}
    _initial_text = {}
    package = None

    def __init__(self, args):
        package = args["package"]
        self.package = package
        if package not in self.exports:
            self.exports[package] = R(
                """
                cat(paste(getNamespaceExports(asNamespace('{}')), collapse = '\n'))
                """.format(package)).strip().split("\n")

    def name(self):
        return "function"

    def initial_text(self):
        if self.package in RideAskFunction._initial_text:
            return RideAskFunction._initial_text[self.package]

    def placeholder(self):
        return "object"

    def confirm(self, text):
        RideAskFunction._initial_text[self.package] = text

    def cancel(self):
        if self.package in RideAskFunction._initial_text:
            del RideAskFunction._initial_text[self.package]

    def list_items(self):
        package = self.package
        if package in self.exports:
            return self.exports[package]

    def next_input(self, args):
        return RideAskArgs(args)


class RideAskArgs(sublime_plugin.TextInputHandler):
    package = None
    function = None
    _initial_text = {}

    def __init__(self, args):
        package = args["package"]
        function = args["function"]
        self.pkgfunc = "{}::{}".format(package, function)

    def name(self):
        return "args"

    def initial_text(self):
        if self.pkgfunc in RideAskArgs._initial_text:
            return RideAskArgs._initial_text[self.pkgfunc]

    def placeholder(self):
        return "args..."

    def preview(self, text):
        return "{}({})".format(self.pkgfunc, text)

    def confirm(self, text):
        RideAskArgs._initial_text[self.pkgfunc] = text

    def cancel(self):
        if self.pkgfunc in RideAskArgs._initial_text:
            del RideAskArgs._initial_text[self.pkgfunc]
