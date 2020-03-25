import sublime

import os
import re

if sublime.platform() == "windows":
    from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE, KEY_READ


PATTERN = re.compile(r"""
    (?P<quote>["'])
    (?P<quoted_var>
        \$ (?: [_a-z][_a-z0-9]*  | \{[^}]*\} )
    )
    (?P=quote)
    |
    (?P<var>
        \$ (?: [_a-z][_a-z0-9]*  | \{[^}]*\} )
    )
""", re.VERBOSE)


def read_registry(key, valueex):
    reg_key = OpenKey(HKEY_LOCAL_MACHINE, key, 0, KEY_READ)
    return QueryValueEx(reg_key, valueex)


def escape_dquote(cmd):
    cmd = cmd.replace('\\', '\\\\')
    cmd = cmd.replace('"', '\\"')
    return cmd


def escape_squote(cmd):
    cmd = cmd.replace('\\', '\\\\')
    cmd = cmd.replace("\'", "\'")
    return cmd


def expand_variables(cmd, extracted_variables):
    def convert(m):
        quote = m.group("quote")
        if quote:
            var = sublime.expand_variables(m.group("quoted_var"), extracted_variables)
            if quote == "'":
                return "'" + escape_squote(var) + "'"
            else:
                return '"' + escape_dquote(var) + '"'
        else:
            return sublime.expand_variables(m.group("var"), extracted_variables)
    cmd = PATTERN.sub(convert, cmd)
    return cmd


def is_package_folder(folder):
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


def get_current_folder(view):
    fname = view.file_name()
    window = view.window()
    if fname:
        fname = os.path.realpath(fname)
        for folder in window.folders():
            if fname.startswith(os.path.realpath(folder) + os.sep):
                return folder
    return None


def find_working_dir(window=None, view=None):
    if not window:
        if view:
            window = view.window()
        else:
            window = sublime.active_window()
    if not window:
        raise RuntimeError("Working Directory not found.")

    if not view:
        view = window.active_view()

    if view and view.file_name():
        folder = get_current_folder(view)
        if folder and is_package_folder(folder):
            return folder

        file_dir = os.path.dirname(view.file_name())
        if os.path.isdir(file_dir):
            return file_dir

    for folder in window.folders():
        if not os.path.isdir(folder):
            continue
        if is_package_folder(folder):
            return folder

    if len(window.folders()) == 0:
        RuntimeError("Working Directory not found.")

    return window.folders()[0]


def is_package_window(window):
    if not window:
        return False
    for folder in window.folders():
        if not os.path.isdir(folder):
            continue
        if is_package_folder(folder):
            return True
    return False


DEFAULT_SELECTOR = ", ".join([
    "meta.package.r",
    "source.r",
    "text.tex.latex.rsweave",
    "text.html.markdown.rmarkdown",
    "source.c++.rcpp"
])


def selector_is_active(selector=DEFAULT_SELECTOR, window=None, view=None):
    if not window:
        if view:
            window = view.window()
        else:
            window = sublime.active_window()
    if not window:
        return False

    if not view:
        view = window.active_view()

    if selector is None:
        selector = DEFAULT_SELECTOR
    selectors = [s.strip() for s in selector.split(",")]
    if "meta.package.r" in selectors and is_package_window(window):
        return True

    if view:
        try:
            pt = view.sel()[0].end()
        except Exception:
            pt = 0
        for s in selectors:
            if s.startswith("meta.package.r "):
                if not is_package_window(window):
                    continue
            if view.match_selector(pt, s.replace("meta.package.r ", "")):
                return True

    return False
