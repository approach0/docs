## About

This is the documentation (English) source for a math-aware search enigne.

This documentation is hosted on
[https://approach0.xyz/docs](https://approach0.xyz/docs).

If you spot a mistake or want to contribute to this documentation,
you are welcome to open a pull request.

## Compile
If you edited the source locally, you can compile and preview your
changes (in HTML) by using `sphinx`.

To install sphinx:
```
$ sudo pip install sphinx
$ sudo pip install recommonmark # for Markdown Editing
```

To compile and preview changes in your default HTML browser:
```
$ sphinx-build -b html -d _build/doctrees . _build/html
$ xdg-open ./_build/html/index.html
```
