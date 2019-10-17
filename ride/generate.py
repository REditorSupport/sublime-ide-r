import sublime
import sublime_plugin
import copy
import json
import os
import threading

from .settings import ride_settings
from .rproject import is_package, is_supported_file


ride_menu = [
    {
        "caption": "R-IDE",
        "id": "R-IDE",
        "children": [
            {
                "caption": "Exec",
                "command": "ride_exec"
            },
            {
                "caption": "-"
            },
            {
                "caption": "Extract Function",
                "command": "ride_extract_function"
            },
            {
                "caption": "-"
            }
        ]
    }
]

ride_build = {
    "keyfiles": ["DESCRIPTION"],
    "target": "ride_exec",
    "cancel": {"kill": True},
    "variants": []
}


def generate_menu(path):
    menu = copy.deepcopy(ride_menu)

    items = ride_settings.get("r_ide_exec_items", [])
    for item in items:
        if "cmd" in item:
            menu[0]["children"].append({
                "caption": item["name"],
                "command": "ride_exec",
                "args": {
                    "cmd": item["cmd"]
                }
            })
        else:
            menu[0]["children"].append({"caption": item["name"]})

    with open(path, 'w') as json_file:
        json.dump(menu, json_file)


def generate_build(path):
    build = copy.deepcopy(ride_build)

    items = ride_settings.get("r_ide_exec_items", [])
    build["variants"] = [x for x in items if x["name"] != "-"]

    with open(path, 'w') as json_file:
        json.dump(build, json_file)


def plugin_loaded():
    build_path = os.path.join(
        sublime.packages_path(), 'User', 'R-IDE', 'R-IDE.sublime-build')

    if not os.path.exists(build_path):
        generate_build(build_path)

    ride_settings.add_on_change("r_ide_exec_items", lambda: generate_build(build_path))


def plugin_unloaded():
    menu_path = os.path.join(
        sublime.packages_path(), 'User', 'R-IDE', 'Main.sublime-menu')

    if os.path.exists(menu_path):
        os.unlink(menu_path)


class RideMenuListener(sublime_plugin.EventListener):
    # TODO: dynamic build and menu based on file types

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

            if is_package(view.window()) or is_supported_file(view):
                generate_menu(menu_path)
            else:
                if os.path.exists(menu_path):
                    os.remove(menu_path)

        self.timer = threading.Timer(0.1, set_main_menu)
        self.timer.start()


class RideRegenerateBuildCommand(sublime_plugin.WindowCommand):
    def run(self):
        build_path = os.path.join(
            sublime.packages_path(), 'User', 'R-IDE', 'R-IDE.sublime-build')
        generate_build(build_path)
