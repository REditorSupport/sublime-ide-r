| SYNTAX TEST "Packages/R-IDE/R Markdown.sublime-syntax"

# Test KITNR-style fenced code blocks

```{bash print=FALSE}
|^^^^^^^^^^^^^^^^^^^^ meta.code-fence.definition.begin.markdown
|^^ punctuation.definition.raw.code-fence.begin.markdown
|  ^ punctuation.definition.raw.code-fence.options.begin.markdown
|   ^^^^ constant.other.language-name.markdown
|       ^^^^^^^^^^^^ meta.options.fenced-kitnr.markdown source.r
|             ^ keyword.operator.assignment.r
|              ^^^^^ constant.language.boolean.false.r
|                   ^ punctuation.definition.raw.code-fence.options.end.markdown
 export x=1
|^^^^^^ markup.raw.code-fence.markdown meta.function-call.identifier.shell support.function.shell
```
|^^ meta.code-fence.definition.end.markdown punctuation.definition.raw.code-fence.end.markdown

foo
| <- - meta.code-fence

```{r}
|^^^^^ meta.code-fence.definition.begin.markdown
|^^ punctuation.definition.raw.code-fence.begin.markdown
|  ^ punctuation.definition.raw.code-fence.options.begin.markdown
|   ^ constant.other.language-name.markdown
|    ^ punctuation.definition.raw.code-fence.options.end.markdown
 function(x) {x + 1}
|^^^^^^^^ markup.raw.code-fence.markdown meta.function.r keyword.declaration.function.r
```
|^^ meta.code-fence.definition.end.markdown punctuation.definition.raw.code-fence.end.markdown

foo
| <- - meta.code-fence

```{python}
|^^^^^^^^^^ meta.code-fence.definition.begin.markdown
|^^ punctuation.definition.raw.code-fence.begin.markdown
|  ^ punctuation.definition.raw.code-fence.options.begin.markdown
|   ^^^^^^ constant.other.language-name.markdown
|         ^ punctuation.definition.raw.code-fence.options.end.markdown
def f():
|   ^ markup.raw.code-fence.markdown meta.function.python entity.name.function.python
  pass
```
|^^ meta.code-fence.definition.end.markdown punctuation.definition.raw.code-fence.end.markdown

foo
| <- - meta.code-fence


# Test inlines

This is H~2~O H^2^O
|        ^^^ markup.subscript.markdown-pandoc
|              ^^^ markup.superscript.markdown-pandoc

This is @foo
|       ^^^^ meta.link.reference.markdown-pandoc
|       ^ constant.other.cite.markdown-pandoc
|        ^^^ keyword.other.cite.markdown-pandoc

This is `r literal=TRUE`
|       ^^^^^^^^^^^^^^^^ markup.raw.inline.markdown
|       ^ punctuation.definition.raw.begin.markdown
|        ^ constant.other.language-name.markdown
|          ^^^^^^^^^^^^ source.r.embedded.markdown
|                 ^ keyword.operator.assignment.r
|                  ^^^^ constant.language.boolean.true.r
|                      ^ punctuation.definition.raw.end.markdown

This is latex $x^2 = 3$
|             ^^^^^^^^^ markup.math.inline.markdown text.tex.latex.embedded.markdown meta.environment.math.block.dollar.latex
|             ^ punctuation.definition.math.begin.latex
|              ^ variable.other.math.tex markup.italic.math.tex
|               ^ punctuation.separator.superscript.tex
|                ^ meta.number.integer.decimal.tex constant.numeric.value.tex
|                  ^ keyword.operator.comparison.tex
|                    ^ meta.number.integer.decimal.tex constant.numeric.value.tex
|                     ^ punctuation.definition.math.end.latex

Inline \[1 + 1\], but escaped \[ 1+1\] or \[1+1 \]
|      ^^^^^^^^^ markup.math.inline.markdown text.tex.latex.embedded.markdown meta.environment.math.block.dollar.latex
|                             ^^ constant.character.escape.markdown
|                                   ^^ constant.character.escape.markdown
|                                         ^^ constant.character.escape.markdown
|                                               ^^ constant.character.escape.markdown

Inline \(1 + 1\), but escaped \( 1+1\) or \(1+1 \)
|      ^^^^^^^^^ markup.math.inline.markdown text.tex.latex.embedded.markdown meta.environment.math.block.dollar.latex
|                             ^^ constant.character.escape.markdown
|                                   ^^ constant.character.escape.markdown
|                                         ^^ constant.character.escape.markdown
|                                               ^^ constant.character.escape.markdown

LaTeX \begin{equation}\overline{Y}_{g,t}\end{equation}.
|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ meta.paragraph.markdown
|     ^^^^^^^^^^^^^^^^ meta.function.begin.latex
|     ^^^^^^ keyword.declaration.environment.begin.latex
|     ^ punctuation.definition.backslash.latex
|           ^^^^^^^^^^ meta.group.brace.tex
|           ^ punctuation.definition.group.brace.begin.tex
|            ^^^^^^^^ variable.parameter.function.latex
|                    ^ punctuation.definition.group.brace.end.tex
|                     ^^^^^^^^^^^^^^^^^^ meta.environment.math.block.latex markup.math.block
|                                       ^^^^^^^^^^^^^^ meta.function.end.latex
|                                       ^^^^ keyword.declaration.environment.end.latex
|                                       ^ punctuation.definition.backslash.latex
|                                           ^^^^^^^^^^ meta.group.brace.tex
|                                           ^ punctuation.definition.group.brace.begin.tex
|                                            ^^^^^^^^ variable.parameter.function.latex
|                                                    ^ punctuation.definition.group.brace.end.tex
