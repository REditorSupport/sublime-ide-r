import sublime
import os

from .utils import read_registry


class RideSettings:
    _r_binary = None

    def get(self, key, default):
        window = sublime.active_window()
        if window:
            view = window.active_view()
            if view:
                r_ide_project_settings = view.settings().get("R-IDE", {})
                if key in r_ide_project_settings:
                    return r_ide_project_settings[key]

        s = sublime.load_settings('R-IDE.sublime-settings')
        return s.get(key, default)

    def add_on_change(self, key, on_change):
        s = sublime.load_settings('R-IDE.sublime-settings')
        s.add_on_change(key, on_change)

    def r_binary(self, default="R"):
        r_binary = self.get("r_binary", None)
        if not r_binary:
            if sublime.platform() == "windows":
                if self._r_binary:
                    r_binary = self._r_binary
                else:
                    try:
                        r_binary = os.path.join(
                            read_registry("Software\\R-Core\\R", "InstallPath")[0],
                            "bin",
                            "R.exe")
                    except Exception:
                        pass
                    self._r_binary = r_binary
        if not r_binary:
            r_binary = default
        return r_binary

    def custom_env(self, key=None):
        env = os.environ.copy()

        paths = self.get("additional_paths", [])
        if sublime.platform() == "osx":
            paths += ["/Library/TeX/texbin"]
        if paths:
            sep = ";" if sublime.platform() == "windows" else ":"
            env["PATH"] = sep.join(paths) + sep + env["PATH"]

        lang = self.get("lang", None)
        if lang:
            env["LANG"] = lang
        elif "LANG" not in env:
            env["LANG"] = "en_US.UTF-8"

        if key:
            return env[key]
        else:
            return env


ride_settings = RideSettings()
