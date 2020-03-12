import sublime

import os
import re

if sublime.platform() == "windows":
    from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE, KEY_READ


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


def is_package_window(window):
    if not window:
        return False
    for folder in window.folders():
        if not os.path.isdir(folder):
            continue
        if is_package_folder(folder):
            return True

    return False


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


def is_supported_file(view, ext=""):
    if not view:
        return False
    try:
        pt = view.sel()[0].end()
    except Exception:
        pt = 0

    scope_map = {
        "r": "source.r",
        "rnw": "text.tex.latex.rsweave",
        "rmarkdown": "text.html.markdown.rmarkdown",
        "rcpp": "source.c++.rcpp"
    }

    if ext:
        scope = scope_map[ext]
    else:
        scope = ",".join(scope_map.values())

    if view.match_selector(pt, scope):
        return True

    return False
