import sublime
import os

from .utils import read_registry


class RideSettings:
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

    def r_binary(self, default="R"):
        r_binary = self.get("r_binary", None)
        if not r_binary and sublime.platform() == "windows":
            r_binary = self.r_binary_windows()
        if not r_binary:
            r_binary = default
        return r_binary

    def r_binary_windows(self):
        try:
            return os.path.join(
                read_registry("Software\\R-Core\\R", "InstallPath")[0],
                "bin",
                "R.exe")
        except Exception:
            pass

    def ride_env(self):
        env = os.environ.copy()

        paths = self.get("additional_paths", [])
        if sublime.platform() == "osx" and os.path.isdir("/Library/TeX/texbin"):
            paths += ["/Library/TeX/texbin"]
        if paths:
            sep = ";" if sublime.platform() == "windows" else ":"
            env["PATH"] = sep.join(paths) + sep + env["PATH"]

        lang = self.get("lang", None)
        if lang:
            env["LANG"] = lang
        elif "LANG" not in env:
            env["LANG"] = "en_US.UTF-8"

        return env


ride_settings = RideSettings()
