# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html): `<MAJOR>.<MINOR>.<PATCH>`.

## [Unreleased]

## [1.0.0] - 2023-09-01

Initial commit from [@Pyvonix](https://github.com/Pyvonix)

### Added

- Mega-Libs: standardize the usage of backends/endpoints `ajax`, `api` and `flow` on Mega-Debrid.eu
  with dedicated objects and offer the possibility of re-use/import them in your own source code.
- Mega-Config: getting of mega-debrid.eu credentials from a config file or environment variables.
- Mega-CLI: to easily use libs from a command line.
- Mega-Worker: celery's functions that run Mega-libs on their own and return result.
- Mega-Web: flask's web interface for interfacing with Mega-Worker.
- Mega-Compose: possibility of launching each component in a container.

[1.0.0]: https://github.com/Pyvonix/Mega-Debrid/releases/tag/v1.0.0
