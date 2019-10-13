import sublime
import sublime_plugin

from .settings import ride_settings
from .rproject import is_package
from .rcommand import R


class RideExecCommand(sublime_plugin.WindowCommand):
    def run(self, kill=False, **kwargs):
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
        env.update({
            "PATH": ride_settings.custom_env("PATH"),
            "LANG": ride_settings.custom_env("LANG")
        })
        kwargs["env"] = env
        kwargs = sublime.expand_variables(kwargs, self.window.extract_variables())
        self.window.run_command("exec", kwargs)

    def input(self, *args):
        return RideRunAskPackage()


class RideRunAskPackage(sublime_plugin.ListInputHandler):
    packages = []
    _initial_text = None

    def name(self):
        return "package"

    def initial_text(self):
        if RideRunAskPackage._initial_text:
            return RideRunAskPackage._initial_text

    def list_items(self):
        if not self.packages:
            self.packages[:] = R(
                "cat(paste(rownames(installed.packages())), sep='\n')").strip().split("\n")
        return self.packages

    def confirm(self, text):
        RideRunAskPackage._initial_text = text

    def cancel(self):
        RideRunAskPackage._initial_text = None

    def placeholder(self):
        return "package::"

    def description(self, value, text):
        return "{}::".format(value)

    def next_input(self, args):
        return RideRunAskFunction(args)


class RideRunAskFunction(sublime_plugin.ListInputHandler):
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
        if self.package in RideRunAskFunction._initial_text:
            return RideRunAskFunction._initial_text[self.package]

    def placeholder(self):
        return "object"

    def confirm(self, text):
        RideRunAskFunction._initial_text[self.package] = text

    def cancel(self):
        if self.package in RideRunAskFunction._initial_text:
            del RideRunAskFunction._initial_text[self.package]

    def list_items(self):
        package = self.package
        if package in self.exports:
            return self.exports[package]

    def next_input(self, args):
        return RideRunAskArgs(args)


class RideRunAskArgs(sublime_plugin.TextInputHandler):
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
        if self.pkgfunc in RideRunAskArgs._initial_text:
            return RideRunAskArgs._initial_text[self.pkgfunc]

    def placeholder(self):
        return "args..."

    def preview(self, text):
        return "{}({})".format(self.pkgfunc, text)

    def confirm(self, text):
        RideRunAskArgs._initial_text[self.pkgfunc] = text

    def cancel(self):
        if self.pkgfunc in RideRunAskArgs._initial_text:
            del RideRunAskArgs._initial_text[self.pkgfunc]
