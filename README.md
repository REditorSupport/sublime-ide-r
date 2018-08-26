R-IDE: Make Sublime Text a prefect IDE for R
------------

<a href="https://www.paypal.me/randy3k/5usd" title="Donate to this project using Paypal"><img src="https://img.shields.io/badge/paypal-donate-blue.svg" /></a>

This is a new iteration of the no-longer-maintained [R-Box](https://github.com/randy3k/R-Box) aiming to utilize the use
  of [language server](https://github.com/REditorSupport/languageserver) + better support R Markdown + better support of R packaging + .....

## Installation

1. Install `languageserver` from CRAN
```R
# install R package languageserver
install.packages("languageserver")
```

2. Install `R-IDE` and `LSP` from Package Control


## Usage

To enable language server for R files. Run `LSP: Enable Language Server Globlly` (or `In Project` if you are working with a project) in Command Palette and select `rlang`. Upon successful execution, you should see a badge called `rlang` in the status bar.
