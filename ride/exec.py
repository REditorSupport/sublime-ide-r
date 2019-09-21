import sublime
import sublime_plugin

from .settings import ride_settings
from .rproject import is_package


class RidePackageExecCommand(sublime_plugin.WindowCommand):
    def is_visible(self):
        return is_package(self.window)

    def run(self, cmd, kill=False, env={}):
        kwargs = {}
        kwargs["cmd"] = [ride_settings.r_binary(), "--slave", "-e", cmd]
        kwargs["working_dir"] = self.window.folders()[0]
        env.update({
            "PATH": ride_settings.custom_env("PATH"),
            "LANG": ride_settings.custom_env("LANG")
        })
        kwargs["env"] = env
        kwargs = sublime.expand_variables(kwargs, self.window.extract_variables())
        kwargs["kill"] = kill
        self.window.run_command("exec", kwargs)
