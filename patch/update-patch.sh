#!/bin/bash

set -e

diff -u <(curl -s -L https://raw.githubusercontent.com/sublimehq/Packages/7ab85554037733cdb54cf8e9c71171a1bbd0918b/Markdown/Markdown.sublime-syntax) ../R\ Markdown.sublime-syntax > R\ Markdown.patch
