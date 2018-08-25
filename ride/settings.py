import sublime
import os
import subprocess

from .utils import read_registry


class RideSettings:
    _r_binary = None
    _custom_env = None
    _additional_paths = []

    def get(self, key, default):
        s = sublime.load_settings('R-IDE.sublime-settings')
        return s.get(key, default)

    def r_binary(self):
        r_binary = self.get("r_binary", self._r_binary)
        if not r_binary:
            if sublime.platform() == "windows":
                try:
                    r_binary = os.path.join(
                        read_registry("Software\\R-Core\\R", "InstallPath")[0],
                        "bin",
                        "R.exe")
                except Exception:
                    pass
        if not r_binary:
            r_binary = "R"
        self._r_binary = r_binary
        return r_binary

    def additional_paths(self):
        additional_paths = self.get("additional_paths", self._additional_paths)
        if not additional_paths:
            if sublime.platform() == "osx":
                additional_paths = subprocess.check_output(
                    "/usr/bin/login -fpql $USER $SHELL -l -c 'echo -n $PATH'",
                    shell=True).decode("utf-8")
                additional_paths = additional_paths.strip().split(":")

        self._additional_paths = additional_paths
        return additional_paths

    def custom_env(self):
        if self._custom_env:
            return self._custom_env
        paths = self.additional_paths()
        if sublime.platform() == "osx":
            paths += ["/Library/TeX/texbin", "/usr/local/bin"]
        env = os.environ.copy()
        if paths:
            sep = ";" if sublime.platform() == "windows" else ":"
            env["PATH"] = env["PATH"] + sep + sep.join(paths)

        self._custom_env = env
        return env


ride_settings = RideSettings()
