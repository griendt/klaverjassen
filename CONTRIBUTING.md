Contributing is recommended and always welcome. Feel free to submit a pull request with your changes, but please
review the recommended contributing guide below.

## Style
 - This repository uses the [Black style](https://github.com/psf/black) throughout its project. Please make sure your code
complies with this styling. You can make sure of this by running `formatting.py`.
 - This repository also aims to be MyPy-compliant. This means all functions should have appropriate type hints.
`formatting.py` will also run MyPy with the desired flags so you can check whether your changes are compliant.
 - Any new pull request should be reflected in `CHANGELOG.md`. If you are unsure in which release your changes will end up,
 use "unreleased".

## Features
 - Features *must* be reflected in Github issues. Before working on new features, please submit an issue first.
Besides tracking progress, this will also give insight in desirability of the feature.
 - The functional specification of any new feature *must* be accompanied by unit tests. The more complete the unit tests,
the better. Pull requests for features without unit tests will not be merged.

## Bugfixes
 - Bugfixes *should* also be reflected in Github issues. However, small patches and very minor bugs may be exempted from
 this rule.
 - A bug fix *must* be accompanied by one or more unit tests that show that the desired functionality was not working as
intended before the fix, but does so after the fix.
