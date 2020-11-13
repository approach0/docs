## Setup
Configure `package.json` file with `name` and `author`, then run:
```
$ sudo pip install sphinx
$ sudo pip install recommonmark # for Markdown Editing
$ sphinx-build -b html -d _build/doctrees . _build/html
$ xdg-open ./_build/html/index.html
```

You may also need to edit Github Actions files under `.github` directory.

## Content Edit
Documentation content source files are all located at `content` directory.

This is an open source documentation, feel free to open a pull request.
