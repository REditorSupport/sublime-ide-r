import sublime

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
