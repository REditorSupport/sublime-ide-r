RIDE: Make Sublime Text a prefect IDE for R

This is a new iteration of the no-longer-maintained [R-Box](https://github.com/randy3k/R-Box) aiming to utilize the use
  of [language server](https://github.com/REditorSupport/languageserver) + better support R Markdown + better support of R packaging + .....

------------

<a href="https://www.paypal.me/randy3k/5usd" title="Donate to this project using Paypal"><img src="https://img.shields.io/badge/paypal-donate-blue.svg" /></a>
<a href="https://gratipay.com/~randy3k/" title="Donate to this project using Gratipay"><img src="https://img.shields.io/badge/gratipay-donate-yellow.svg" /></a>


Improve your R coding experiences with Sublime Text!


**Advanced user only (for the moment):  you need to also install [LSP](https://github.com/tomv564/LSP) and [language server](https://github.com/REditorSupport/languageserver) in order to use RIDE.**

```
# mac
cd "$HOME/Library/Application Support/Sublime Text 3/Packages"
# linux
cd $HOME/.config/sublime-text-3/Packages
# windows (PowerShell)
cd "$env:appdata\Sublime Text 3\Packages\"

git clone git@github.com:REditorSupport/sublime-ide-r.git RIDE

# LSP master is also required (as 2018-5-19)
git clone git@github.com:tomv564/LSP.git
```

```
# install R package languageserver
install.packages("languageserver")
```
