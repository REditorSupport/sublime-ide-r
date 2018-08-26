import sublime
import sublime_plugin
import os

from .settings import ride_settings


class RideRenderRmarkdownCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return self.view.settings().get("syntax").endswith("R Markdown.sublime-syntax")

    def run(self, edit):
        cmd = "rmarkdown::render(\"$file\", encoding = \"UTF-8\")"
        kwargs = {}
        kwargs["cmd"] = [ride_settings.r_binary(), "--slave", "-e", cmd]
        kwargs["working_dir"] = os.path.dirname(self.view.file_name())
        kwargs["env"] = {"PATH": ride_settings.custom_env("PATH")}
        kwargs = sublime.expand_variables(kwargs, self.view.window().extract_variables())
        self.view.window().run_command("exec", kwargs)


class RideSweaveRnwCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return self.view.settings().get("syntax").endswith("R Sweave.sublime-syntax")

    def run(self, edit):
        cmd = ("""Sweave(\"$file\")\n"""
               """tools::texi2dvi(\"$file_base_name.tex\", pdf = TRUE)""")
        kwargs = {}
        kwargs["cmd"] = [ride_settings.r_binary(), "--slave", "-e", cmd]
        kwargs["working_dir"] = os.path.dirname(self.view.file_name())
        kwargs["env"] = {"PATH": ride_settings.custom_env("PATH")}
        kwargs = sublime.expand_variables(kwargs, self.view.window().extract_variables())
        self.view.window().run_command("exec", kwargs)


class RideKnitRnwCommand(sublime_plugin.TextCommand):
    def is_enabled(self):
        return self.view.settings().get("syntax").endswith("R Sweave.sublime-syntax")

    def run(self, edit):
        cmd = ("""knitr::knit(\"$file\", output=\"$file_base_name.tex\")\n"""
               """tools::texi2dvi(\"$file_base_name.tex\", pdf = TRUE)")""")
        kwargs = {}
        kwargs["cmd"] = [ride_settings.r_binary(), "--slave", "-e", cmd]
        kwargs["working_dir"] = os.path.dirname(self.view.file_name())
        kwargs["env"] = {"PATH": ride_settings.custom_env("PATH")}
        kwargs = sublime.expand_variables(kwargs, self.view.window().extract_variables())
        self.view.window().run_command("exec", kwargs)
