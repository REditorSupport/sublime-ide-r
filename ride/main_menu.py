import sublime
import sublime_plugin
import os
from shutil import copyfile
import threading

from .settings import ride_settings


_main_menu_is_visible = [False]
_window_is_rproject = []
_window_is_not_rproject = []
_window_folders = {}


def main_menu_is_visible():
    return _main_menu_is_visible[0]


class RideMainMenuListener(sublime_plugin.EventListener):
    def window_is_rproj(self, folders):
        for folder in folders:
            if not os.path.isdir(folder):
                continue
            for f in os.listdir(folder):
                if f.endswith(".Rproj"):
                    return True

            description_file = os.path.join(folder, "DESCRIPTION")
            namespace_file = os.path.join(folder, "NAMESPACE")
            r_source_dir = os.path.join(folder, "R")
            if os.path.isfile(description_file) and os.path.isfile(namespace_file) \
                    and os.path.isdir(r_source_dir):
                return True

        return False

    def is_r_project(self, window):
        if not window:
            return False
        folders = window.folders()

        if folders:
            if window.id() in _window_folders and _window_folders[window.id()] == folders:
                if window.id() in _window_is_rproject:
                    return True
                elif window.id() in _window_is_not_rproject:
                    return False

            _window_folders[window.id()] = folders

            if self.window_is_rproj(folders):
                _window_is_rproject.append(window.id())
                return True
            else:
                _window_is_not_rproject.append(window.id())
                return False

        return False

    def is_r_file(self, view):
        try:
            pt = view.sel()[0].end()
        except Exception:
            pt = 0

        if view.match_selector(pt, "source.r, "
                               "text.tex.latex.rsweave, "
                               "text.html.markdown.rmarkdown, "
                               "source.c++.rcpp"):
            return True

        return False

    def on_activated_async(self, view):
        if view.settings().get('is_widget'):
            return
        if hasattr(self, "timer") and self.timer:
            self.timer.cancel()

        if not ride_settings.get("r_ide_menu", False):
            return

        def set_main_menu():

            menu_path = os.path.join(
                sublime.packages_path(), 'User', 'R-IDE', 'Main.sublime-menu')
            user_menu_path = os.path.join(
                sublime.packages_path(), 'User', 'R-IDE', 'R-IDE.sublime-menu')
            menu_dir = os.path.dirname(menu_path)

            if self.is_r_project(view.window()) or self.is_r_file(view):

                if not os.path.exists(menu_dir):
                    os.makedirs(menu_dir, 0o755)

                if not os.path.exists(menu_path):
                    if os.path.exists(user_menu_path):
                        copyfile(user_menu_path, menu_path)
                    else:
                        data = sublime.load_resource(
                            "Packages/R-IDE/support/R-IDE.sublime-menu")
                        with open(menu_path, 'w') as f:
                            f.write(data.replace("\r\n", "\n"))
                            f.close()
                _main_menu_is_visible[0] = True
            else:
                if os.path.exists(menu_path):
                    os.remove(menu_path)
                _main_menu_is_visible[0] = False

        self.timer = threading.Timer(0.1, set_main_menu)
        self.timer.start()


class RidePackageExecCommand(sublime_plugin.WindowCommand):
    def is_visible(self):
        return self.window.id() in _window_is_rproject

    def run(self, cmd):
        kwargs = {}
        kwargs["cmd"] = [ride_settings.r_binary(), "--slave", "-e", cmd]
        kwargs["working_dir"] = self.window.folders()[0]
        kwargs["env"] = {"PATH": ride_settings.custom_env("PATH")}
        kwargs = sublime.expand_variables(kwargs, self.window.extract_variables())
        self.window.run_command("exec", kwargs)


def plugin_unload():
    menu_path = os.path.join(
        sublime.packages_path(), 'User', 'R-IDE', 'Main.sublime-menu')
    if os.path.exists(menu_path):
        os.remove(menu_path)
