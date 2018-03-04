# Information for contributors

## Development environment

* [Code and Issues are at Github](http://github.com/severinsimmler/forpus)

### Start hacking

```bash
$ git clone -b testing git@github.com:severinsimmler/forpus
$ cd forpus
$ mkvirtualenv forpus      # if you use virtualenvwrapper
$ workon forpus            # if you use virtualenvwrapper
$ pip install -r requirement-dev.txt
```

### Running the tests

Installing from `requirements-dev.txt` also installs the testing framework `pytest`, which is configured in `setup.cfg`. You can run the tests locally from the command line:

* `pytest` runs all unit tests (functions starting/ending with `test_` or `_test`, respectively) as well as all doctests. At the time of writing, these are 52 tests, taking ~3s in total.
* `pytest --nbsmoke-run` additionally runs all Jupyter Notebooks and reports errors. This takes significantly longer (~90s).


## Releasing

The `develop` branch is the integration branch for current developments. The `master` branch should always contain the latest stable version. 

To push from `develop` to `master`, do the following (from a clean working copy):

1. Prepare everything in `develop`. Don't forget to tune the version number.
2. Merge `develop` into `master`. Use `--no-ff` to make sure we get a merge commit: `git checkout master; git merge --no-ff develop`
3. If there are conflicts, resolve them and commit (to `master`).
4. Now, fast-forward-merge `master` into `develop`: `git checkout develop; git merge master`.
5. Push `develop`, then push `master`.

If something goes wrong, `git reset --hard master origin/master` and try again.


## Documentation

The documentation is built using [Sphinx](http://www.sphinx-doc.org/). 
The following files influence the docs:

* ``index.rst`` contains the landing page with the table of contents. Here, all files should be linked.
* ``*.ipynb`` for tutorials etc. can be linked from the index file.
* ``README.md`` and ``CONTRIBUTING.md`` will also be included.
* Docstrings in the modules will be included.
* ``docs/**/*`` may contain additional files.
* ``conf.py`` contains Sphinx configuration.
* ``setup.py`` contains version numbers, etc.

### Documentation formats

Standalone documentation files can be written in one of the following formats:

* ReSTructured Text (`*.rst`), [see Sphinx docs](http://www.sphinx-doc.org/en/stable/rest.html)
* Jupyter Notebook (`*.ipynb`), by way of [nbsphinx](https://nbsphinx.readthedocs.io/)
* Markdown

Docstrings should follow [Google conventions](http://google.github.io/styleguide/pyguide.html?showone=Comments#Comments), this is supported by [Napoleon](http://www.sphinx-doc.org/en/stable/ext/napoleon.html).

### Build the documentation

Run `python setup.py build_sphinx -a`, which will create the documentation tree in `build/sphinx/html`.
