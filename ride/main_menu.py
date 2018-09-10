import sublime
import sublime_plugin
import os
from shutil import copyfile
import threading

from .settings import ride_settings
from .rproject import is_package, is_supported_file

_main_menu_is_visible = [False]


def main_menu_is_visible():
    return _main_menu_is_visible[0]


class RideMainMenuListener(sublime_plugin.EventListener):

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

            if is_package(view.window()) or is_supported_file(view):

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


def plugin_unloaded():
    menu_path = os.path.join(
        sublime.packages_path(), 'User', 'R-IDE', 'Main.sublime-menu')
    if os.path.exists(menu_path):
        os.remove(menu_path)
