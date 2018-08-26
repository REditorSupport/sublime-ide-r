import sublime

if sublime.platform() == "windows":
    from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE, KEY_READ


def read_registry(key, valueex):
    reg_key = OpenKey(HKEY_LOCAL_MACHINE, key, 0, KEY_READ)
    return QueryValueEx(reg_key, valueex)


def escape_dquote(cmd):
    cmd = cmd.replace('\\', '\\\\')
    cmd = cmd.replace('"', '\\"')
    return cmd
