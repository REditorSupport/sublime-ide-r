import sublime
import re
import os
import subprocess
from .utils import find_working_dir
from .settings import ride_settings

ANSI_ESCAPE = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
message_shown = [False]


def R(script=None, file=None, args=None, stdin_text=None,
        slave=True, quiet=True, working_dir=None):
    cmd = [ride_settings.r_binary()]
    if slave:
        cmd = cmd + ["--slave"]
    elif quiet:
        cmd = cmd + ["--quiet"]
    if script:
        cmd = cmd + ["-e", script]
    elif file:
        cmd = cmd + ["-f", file]
    if args:
        cmd = cmd + args

    if sublime.platform() == "windows":
        # make sure console does not come up
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    else:
        startupinfo = None

    if not working_dir:
        working_dir = find_working_dir()
    ride_env = ride_settings.ride_env()

    try:
        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=working_dir,
            env=ride_env,
            startupinfo=startupinfo,
            universal_newlines=True)

        stdout, stderr = p.communicate(input=stdin_text)

        if p.returncode == 0:
            return ANSI_ESCAPE.sub('', stdout)
        else:
            raise Exception(
                "Failed to execute RScript with the following output:\n\n{}".format(stderr))

    except FileNotFoundError:
        if not message_shown[0]:
            sublime.message_dialog(
                "R binary cannot be found automatically. "
                "The path to `R` can be specified in the R-IDE settings.")
            message_shown[0] = True
        raise Exception("R binary not found.")
