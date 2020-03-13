import sublime
import sublime_plugin
import copy
import json
import os
import threading

from ..settings import ride_settings
from ..utils import selector_is_active


ride_menu = [
    {
        "caption": "R-IDE",
        "id": "R-IDE",
        "children": [
            {
                "caption": "Extract Function",
                "command": "ride_extract_function"
            },
            {
                "caption": "-"
            },
            {
                "caption": "Exec",
                "command": "ride_exec"
            },
            {
                "caption": "-"
            },
        ]
    }
]

ride_build = {
    "keyfiles": ["DESCRIPTION"],
    "selector": "source.r, text.tex.latex.rsweave, text.html.markdown.rmarkdown, source.c++.rcpp",
    "target": "ride_exec",
    "cancel": {"kill": True},
    "variants": []
}


def generate_menu(path):
    menu = copy.deepcopy(ride_menu)
    menu_items = ride_settings.get("menu_items", [])
    if menu_items:
        menu[0]["children"].insert(2, {"caption": "-"})
    for item in reversed(menu_items):
        menu[0]["children"].insert(2, item)

    exec_items = ride_settings.get("exec_items", [])
    for item in exec_items:
        caption = item["caption"] if "caption" in item else item["name"]
        if "cmd" in item:
            args = {
                "cmd": item["cmd"],
                "selector": item["selector"] if "selector" in item else ""
            }
            if "file_regex" in item:
                args["file_regex"] = item["file_regex"]
            if "working_dir" in item:
                args["working_dir"] = item["working_dir"]
            if "subdir" in item:
                args["subdir"] = item["subdir"]
            menu[0]["children"].append({
                "caption": caption,
                "command": "ride_exec",
                "args": args
            })
        else:
            menu[0]["children"].append({"caption": caption})

    pathdir = os.path.dirname(path)
    if not os.path.exists(pathdir):
        os.makedirs(pathdir, 0o755)
    with open(path, 'w') as json_file:
        json.dump(menu, json_file)


def generate_build(path, view):
    build = copy.deepcopy(ride_build)

    items = ride_settings.get("exec_items", [])
    for item in items:
        caption = item["caption"] if "caption" in item else item["name"]
        if caption == "-":
            continue
        if "selector" in item and not selector_is_active(item["selector"], view=view):
            continue
        v = {
            "name": caption,
            "cmd": item["cmd"]
        }
        if "file_regex" in item:
            v["file_regex"] = item["file_regex"]
        if "working_dir" in item:
            v["working_dir"] = item["working_dir"]
        if "subdir" in item:
            v["subdir"] = item["subdir"]
        build["variants"].append(v)

    pathdir = os.path.dirname(path)
    if not os.path.exists(pathdir):
        os.makedirs(pathdir, 0o755)
    with open(path, 'w') as json_file:
        json.dump(build, json_file)


def plugin_unloaded():
    menu_path = os.path.join(
        sublime.packages_path(), 'User', 'R-IDE', 'Main.sublime-menu')
    if os.path.exists(menu_path):
        os.unlink(menu_path)

    build_path = os.path.join(
        sublime.packages_path(), 'User', 'R-IDE', 'R-IDE.sublime-build')
    if os.path.exists(build_path):
        os.unlink(build_path)


class RideDynamicMenuListener(sublime_plugin.EventListener):
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

            if selector_is_active(view=view):
                if not os.path.exists(menu_path):
                    generate_menu(menu_path)
            else:
                if os.path.exists(menu_path):
                    os.remove(menu_path)

        self.timer = threading.Timer(0.5, set_main_menu)
        self.timer.start()


class RideDynamicBuildListener(sublime_plugin.EventListener):
    def on_activated_async(self, view):
        if view.settings().get('is_widget'):
            return

        if not selector_is_active(view=view):
            return

        if hasattr(self, "timer") and self.timer:
            self.timer.cancel()

        def set_build():
            build_path = os.path.join(
                sublime.packages_path(), 'User', 'R-IDE', 'R-IDE.sublime-build')
            generate_build(build_path, view=view)

        self.timer = threading.Timer(0.5, set_build)
        self.timer.start()
