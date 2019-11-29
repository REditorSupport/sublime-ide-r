#!/bin/bash

set -e


diff -u <(curl -s -L https://raw.githubusercontent.com/sublimehq/Packages/759d6eed9b4beed87e602a23303a121c3a6c2fb3/Markdown/Markdown.sublime-syntax) ../R\ Markdown.sublime-syntax > R\ Markdown.patch
