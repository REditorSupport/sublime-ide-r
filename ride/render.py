import sublime
import sublime_plugin
import os

from .settings import ride_settings


class RideRenderRmarkdownCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        view = self.window.active_view()
        return view.settings().get("syntax").endswith("R Markdown.sublime-syntax")

    def run(self, kill=False):
        cmd = "rmarkdown::render(\"$file_name\", encoding = \"UTF-8\")"
        cmd = sublime.expand_variables(cmd, self.window.extract_variables())
        kwargs = {}
        kwargs["cmd"] = [ride_settings.r_binary(), "--slave", "-e", cmd]
        kwargs["working_dir"] = os.path.dirname(self.window.active_view().file_name())
        kwargs["env"] = {
            "PATH": ride_settings.custom_env("PATH"),
            "LANG": ride_settings.get("lang", "en_US.UTF-8")
        }
        kwargs["kill"] = kill
        self.window.run_command("exec", kwargs)


class RideSweaveRnwCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        view = self.window.active_view()
        return view.settings().get("syntax").endswith("R Sweave.sublime-syntax")

    def run(self, kill=False):
        cmd = ("""Sweave(\"$file_name\");"""
               """tinytex::latexmk(\"$file_base_name.tex\")""")
        cmd = sublime.expand_variables(cmd, self.window.extract_variables())
        kwargs = {}
        kwargs["cmd"] = [ride_settings.r_binary(), "--slave", "-e", cmd]
        kwargs["working_dir"] = os.path.dirname(self.window.active_view().file_name())
        kwargs["env"] = {
            "PATH": ride_settings.custom_env("PATH"),
            "LANG": ride_settings.get("lang", "en_US.UTF-8")
        }
        kwargs["kill"] = kill
        self.window.run_command("exec", kwargs)


class RideKnitRnwCommand(sublime_plugin.WindowCommand):
    def is_enabled(self):
        view = self.window.active_view()
        return view.settings().get("syntax").endswith("R Sweave.sublime-syntax")

    def run(self, kill=False):
        cmd = "knitr::knit2pdf(\"$file_name\")"
        cmd = sublime.expand_variables(cmd, self.window.extract_variables())
        kwargs = {}
        kwargs["cmd"] = [ride_settings.r_binary(), "--slave", "-e", cmd]
        kwargs["working_dir"] = os.path.dirname(self.window.active_view().file_name())
        kwargs["env"] = {
            "PATH": ride_settings.custom_env("PATH"),
            "LANG": ride_settings.get("lang", "en_US.UTF-8")
        }
        kwargs["kill"] = kill
        self.window.run_command("exec", kwargs)
