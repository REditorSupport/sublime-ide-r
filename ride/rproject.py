import os


def is_package(window):
    for folder in window.folders():
        if not os.path.isdir(folder):
            continue
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


def is_supported_file(view):
    try:
        pt = view.sel()[0].end()
    except Exception:
        pt = 0

    if view.match_selector(pt, "source.r, "
                           "text.tex.latex.rsweave, "
                           "text.html.markdown.rmarkdown, "
                           "source.c++.rcpp"):
        return True

    return False
