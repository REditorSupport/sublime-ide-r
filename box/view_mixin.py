import re
import sublime

VALIDCALL = re.compile(r"(?:([a-zA-Z][a-zA-Z0-9.]*)(?::::?))?([.a-zA-Z0-9_-]+)\s*\($")


class RBoxViewMixin:

    def function_name_at_point(self, view, pt):
        if not view.match_selector(pt, "meta.function-call.r"):
            return None, None
        scope_begin = view.extract_scope(pt).begin()
        if view.match_selector(scope_begin, "support.function.r, variable.function.r"):
            scope_begin = view.find("\(", scope_begin).begin() + 1
        line = self.extract_line(view, scope_begin, truncated=True)
        m = VALIDCALL.search(line)
        if m:
            return m.groups()
        else:
            return None, None

    def _render_from_mdpopups_view(self, view):
        mdpops_view = view.window().find_output_panel("mdpopups")
        parameters_scope = "source.r meta.function-call.r " \
            "meta.function-call.parameters.r "
        var_scope = "source.r meta.function-call.r " \
            "meta.function-call.parameters.r variable.parameter.r "
        comma_scope = "source.r meta.function-call.r " \
            "meta.function-call.parameters.r punctuation.separator.parameters.r "
        parameters_regeion = mdpops_view.find_by_selector(parameters_scope)
        replacements = []
        if len(parameters_regeion) > 0:
            begin = parameters_regeion[0].begin()
            end = parameters_regeion[0].end()
            pt = begin
            count = 1
            while pt < end:
                pt = mdpops_view.find(r"\S", pt).begin()
                kwarg = False
                if mdpops_view.scope_name(pt) == var_scope:
                    kwarg = True
                    parapt = mdpops_view.find(r"=", pt).begin()
                    parapt = mdpops_view.find(r"\S", parapt + 1).begin()

                seppt = pt
                while True:
                    seppt = mdpops_view.find(",", seppt + 1).begin()
                    if seppt > 0 and mdpops_view.scope_name(seppt) == comma_scope:
                        break

                    if seppt == -1:
                        seppt = end
                        break

                if kwarg:
                    orig_var = mdpops_view.substr(sublime.Region(pt, parapt))
                    orig_text = mdpops_view.substr(sublime.Region(parapt, seppt))
                    text = "${%d:%s${%d:%s}}" % (count, orig_var, count + 1, orig_text)
                    count = count + 2
                else:
                    orig_text = mdpops_view.substr(sublime.Region(pt, seppt))
                    text = "${%d:%s}" % (count, orig_text)
                    count = count + 1

                replacements.append([pt, seppt, text])
                pt = seppt + 1

            for begin, end, text in reversed(replacements):
                mdpops_view.run_command(
                    "r_box_replace_selection",
                    {"region": (begin, end), "text": format(text)})

        return mdpops_view.substr(sublime.Region(0, mdpops_view.size()))

    def replace_function_at_point(self, view, point):
        text = self._render_from_mdpopups_view(view)
        text = " ".join([x.strip() for x in text.split("\n")])
        function_region = view.extract_scope(point)
        view.sel().clear()
        view.sel().add(function_region)
        view.run_command("insert_snippet", {"contents": text})

    def inline_packages_for_view(self, view):
        packages = []
        for s in view.find_all(r"""(library|require)\(["']?[a-zA-Z][a-zA-Z0-9.]*"""):
            pkg = packages.append(re.sub(r"""(library|require)\(["']?""", "", view.substr(s)))
            if pkg and pkg not in packages:
                packages.append(pkg)
        return packages

    def extract_line(self, view, pt, truncated=False):
        if truncated:
            row, _ = view.rowcol(pt)
            line_begin = view.text_point(row, 0)
            return view.substr(sublime.Region(line_begin, pt))
        else:
            return view.substr(view.line(pt))
