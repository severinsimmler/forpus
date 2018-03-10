# Information for contributors

## Development environment

* [Code and Issues are at GitHub](http://github.com/severinsimmler/forpus)

### Start hacking

```bash
$ git clone -b develop git@github.com:severinsimmler/forpus
$ cd forpus
$ mkvirtualenv forpus      # if you use virtualenvwrapper
$ workon forpus            # if you use virtualenvwrapper
$ pip install -r requirements-dev.txt
```

### Running the tests

Installing from `requirements-dev.txt` also installs the testing framework `pytest`. You can run the tests locally from the command-line:

* `pytest` runs all unit tests. At the time of writing, these are 16 tests, taking ~1.3s in total.

## Releasing

The `develop` branch is the integration branch for current developments. The `master` branch should always contain the latest stable version. 

To push from `develop` to `master`, do the following (from a clean working copy):

1. Prepare everything in `develop`. Don't forget to tune the version number.
2. Merge `develop` into `master`. Use `--no-ff` to make sure we get a merge commit: `git checkout master; git merge --no-ff develop`
3. If there are conflicts, resolve them and commit (to `master`).
4. Now, fast-forward-merge `master` into `develop`: `git checkout develop; git merge master`.
5. Push `develop`, then push `master`.

If something goes wrong, `git reset --hard master origin/master` and try again.


### Documentation formats

Standalone documentation files can be written in one of the following formats:

* ReSTructured Text (`*.rst`), [see Sphinx docs](http://www.sphinx-doc.org/en/stable/rest.html)

Docstrings should follow [Google conventions](http://google.github.io/styleguide/pyguide.html?showone=Comments#Comments), this is supported by [Napoleon](http://www.sphinx-doc.org/en/stable/ext/napoleon.html).
