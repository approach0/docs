## Setup
Configure `package.json` file with `name` and `author`, then run:
```
$ sudo pip install sphinx
$ sudo pip install recommonmark # for Markdown Editing
$ sphinx-build -b html -d _build/doctrees . _build/html
$ xdg-open ./_build/html/index.html
```

Please note: NPM package naming is somewhat very restricted.
It only allows lowercase and no space (see [this link](https://docs.npmjs.com/cli/v6/configuring-npm/package-json)),otherwise `npm install` will not install any package.
As a result, in `conf.py` we convert package name to uppercase and `_` to space so that it will display nicely as HTML page title.

You may also need to edit Github Actions files under `.github` directory.
(And perhaps add a github project SECRET for webhook authentication)

## How to edit content?
Documentation content source files are all located at `content` directory.

This is an open source documentation, feel free to open a pull request.
