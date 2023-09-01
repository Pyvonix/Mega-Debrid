# Contributing to [Mega-Debrid](https://github.com/Pyvonix/Mega-Debrid)

All contributions are welcome on this repository!

Before contributing and submitting your pull request, please make sure to discuss
the change you wish via an issue with the owner or others users of this repository.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## How can I contribute to this project?

- Bug fixes
- Code cleaning or code refactoring
- Documentation improvements
- Feature requests

## Pull Request Process

1. Ensure unnecessary dependencies and dead code are removed.
2. Format the source code with [Black](https://black.readthedocs.io/en/stable/).
3. Verify that unit tests pass and for new feature make sure to cover it with the appropriate test.
4. Update the `README.md` with details that need to be metionned to users, this includes for CLI: new command,
   and new parameters, new environment variables, exposed ports, useful file locations and container parameters.
5. Create a new entry in [CHANGELOG.md](./CHANGELOG.md) with the new version describing the changes.
   The versioning convention used is [SemVer](https://semver.org/): `<MAJOR>.<MINOR>.<PATCH>`. \
   Defined as follows:
   - `MAJOR` version changes represent a significant change to the fundamental architecture of Mega-Debrid and may (but don't always) make breaking changes that are not backwards compatible.
   - `MINOR` version changes usually mean the addition of new operations or reasonably significant new features.
   - `PATCH` versions are used for bug fixes and any other small tweaks that modify or improve existing capabilities.
6. You may merge the Pull Request in once you have the sign-off from two other developers, or if you
   do not have permission to do that, you may request the second reviewer to merge it for you.
