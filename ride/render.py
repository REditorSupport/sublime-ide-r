import sublime
import sublime_plugin
import os

from .settings import ride_settings
from .utils import expand_variables


class RideRenderRmarkdownCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        view = self.window.active_view()
        return view.settings().get("syntax").endswith("R Markdown.sublime-syntax")

    def run(self):
        cmd = "rmarkdown::render(\"$file\", encoding = \"UTF-8\")"
        extracted_variables = self.window.extract_variables()
        cmd = expand_variables(cmd, extracted_variables)
        kwargs = {}
        kwargs["cmd"] = [ride_settings.r_binary(), "--slave", "-e", cmd]
        kwargs["working_dir"] = os.path.dirname(self.window.active_view().file_name())
        kwargs["env"] = {"PATH": ride_settings.custom_env("PATH")}
        kwargs = sublime.expand_variables(kwargs, self.window.extract_variables())
        self.window.run_command("exec", kwargs)


class RideSweaveRnwCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        view = self.window.active_view()
        return view.settings().get("syntax").endswith("R Sweave.sublime-syntax")

    def run(self, edit):
        cmd = ("""Sweave(\"$file\")\n"""
               """tools::texi2dvi(\"$file_base_name.tex\", pdf = TRUE)""")
        extracted_variables = self.window.extract_variables()
        cmd = expand_variables(cmd, extracted_variables)
        kwargs = {}
        kwargs["cmd"] = [ride_settings.r_binary(), "--slave", "-e", cmd]
        kwargs["working_dir"] = os.path.dirname(self.window.active_view().file_name())
        kwargs["env"] = {"PATH": ride_settings.custom_env("PATH")}
        kwargs = sublime.expand_variables(kwargs, self.window.extract_variables())
        self.window.run_command("exec", kwargs)


class RideKnitRnwCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        view = self.window.active_view()
        return view.settings().get("syntax").endswith("R Sweave.sublime-syntax")

    def run(self, edit):
        cmd = ("""knitr::knit(\"$file\", output=\"$file_base_name.tex\")\n"""
               """tools::texi2dvi(\"$file_base_name.tex\", pdf = TRUE)")""")
        extracted_variables = self.window.extract_variables()
        cmd = expand_variables(cmd, extracted_variables)
        kwargs = {}
        kwargs["cmd"] = [ride_settings.r_binary(), "--slave", "-e", cmd]
        kwargs["working_dir"] = os.path.dirname(self.window.active_view().file_name())
        kwargs["env"] = {"PATH": ride_settings.custom_env("PATH")}
        kwargs = sublime.expand_variables(kwargs, self.window.extract_variables())
        self.window.run_command("exec", kwargs)
