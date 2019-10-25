R-IDE: Make Sublime Text a perfect IDE for R
------------

<a href="https://www.paypal.me/randy3k/5usd" title="Donate to this project using Paypal"><img src="https://img.shields.io/badge/paypal-donate-blue.svg" /></a>

This is a new iteration of the no-longer-maintained [R-Box](https://github.com/randy3k/R-Box) aiming to utilize the use
  of [language server](https://github.com/REditorSupport/languageserver) + better support R Markdown + better support of R packaging + .....

## Installation

1. Install [`languageserver`](https://github.com/REditorSupport/languageserver) from CRAN
```R
# install R package languageserver
install.packages("languageserver")
```

2. Install `R-IDE` and [`LSP`](https://github.com/tomv564/LSP) from Package Control


## Usage

- language features for R files

    Execute `LSP: Enable Language Server Globally` (or `In Project` if you are working with a project) in Command Palette and enable `rlang`. Upon successful execution, you should see a badge called `rlang` in the status bar.

- language features for C/C++ files
    
    `R-IDE` ultilizes [`ccls`](https://github.com/MaskRay/ccls) to provide language features for C/C++ files. Install `ccls` first. Then enable `ccls-r` server in LSP.

- R-IDE menu

    There is a R-IDE menu when an R project or an R file is opened. User could edit the setting `exec_items` to modify the menu.

    <img width="240" alt="Screen Shot 2019-10-18 at 7 20 49 PM" src="https://user-images.githubusercontent.com/1690993/67136543-789a7b80-f1dc-11e9-9156-98d2e64e25fd.png">

- Build system

    Hit `cmd/ctrl+b` to launch the predefined commands. Use the setting `exec_items` to modify the items.

- R-IDE Exec

    User could run any R functions via `R-IDE: Exec`.


## Recommendations

- [SendCode](https://github.com/randy3k/SendCode) for sending R code to Terminal / R GUI / RStudio.
- [Bracket​Highlighter](https://github.com/facelessuser/BracketHighlighter) for advanced bracket highlighting.
- [Whitespace](https://github.com/randy3k/Whitespace) for cleaning whitespaces.
- [Terminus](https://github.com/randy3k/Terminus) for running R Console in Sublime Text.
- [radian](https://github.com/randy3k/radian) is a better R console for Terminal.
