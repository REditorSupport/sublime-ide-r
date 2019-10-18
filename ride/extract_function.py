import sublime
import sublime_plugin
import tempfile
import re
import os

from .rcommand import R


class RideExtractFunctionCommand(sublime_plugin.TextCommand):
    def run(self, edit, func_name=None):
        if not func_name:
            self.view.window().show_input_panel(
                "Function name:", "",
                lambda x: self.view.run_command("ride_extract_function", {"func_name": x}),
                None, None)
            return

        sels = self.view.sel()
        if len(sels) == 0 or len(sels) > 1:
            return

        region = self.view.sel()[0]
        indentation = re.match(
            r"^\s*", self.view.substr(self.view.line(region.begin()))).group(0)

        if region.empty():
            code = self.view.substr(self.view.line(region.begin()))
        else:
            code = self.view.substr(
                sublime.Region(
                    self.view.line(region.begin()).begin(),
                    self.view.line(region.end()).end()))

        try:
            free_vars = self.detect_free_vars(code)

            self.view.insert(edit,
                             self.view.line(region.end()).end(),
                             "\n{}}}\n".format(indentation))

            self.view.insert(edit,
                             self.view.line(region.begin()).begin(),
                             "{}{} <- function({}) {{\n".format(
                                 indentation, func_name, ", ".join(free_vars)))

            self.view.run_command("indent")
            sublime.status_message("Extract function successed.")

        except Exception as e:
            print(e)
            sublime.status_message("Extract function failed.")

    def detect_free_vars(self, code):
        dfv_path = tempfile.mkstemp(suffix=".R")[1]
        data = sublime.load_resource("Packages/R-IDE/ride/detect_free_vars.R")
        with open(dfv_path, 'w') as f:
            f.write(data.replace("\r\n", "\n"))
            f.close()

        result = R(
            file=dfv_path,
            stdin_text=code
        ).strip()

        try:
            os.unlink(dfv_path)
        except Exception:
            pass

        return [s.strip() for s in result.split("\n")] if result else []

    def is_enabled(self, **kwargs):
        view = self.view
        try:
            pt = view.sel()[0].end()
        except Exception:

            pt = 0
        if not view.match_selector(pt, "source.r"):
            return False

        if all(s.empty() for s in view.sel()):
            return False

        return True
