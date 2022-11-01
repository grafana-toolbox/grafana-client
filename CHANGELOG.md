# CHANGELOG

## unreleased


## 3.2.0 (2022-11-01)

* Implement foundation for accessing the Alerting Provisioning API.
  Thanks, @bursztyn-pl.


## 3.1.0 (2022-09-15)

* Update the `update_folder` method of the folder API to allow changing
  the UID of the folder. Thanks, @iNoahNothing.
* Add `update_datasource_by_uid` to the datasource API. Thanks, @mgreen-sm.
* Add `HeaderAuth` authentication mechanism, using an arbitrary HTTP header for
  authentication, where the user can specify both its name and value. Thanks, @l0tzi.


## 3.0.0 (2022-07-02)

* Add example program `examples/team.py`. Thanks, @ricmano!
* Improve data source API by adding the `_by_uid` variants.
* Improve data source API by adding universal `datasource.get()` method.
* Improve data source API by adding a data source health-check probe.
* Support data source health check endpoint introduced with Grafana 9.
  Thanks, @jangaraj!
* Add gracefulness when using the new data source health check endpoint.
  Apparently, this is not implemented thoroughly for all data source types yet.
* Add new factory methods `GrafanaApi.{from_url(),from_env()}`.
* Add `GrafanaApi.connect()` and `GrafanaApi.version()`.
* Data source health check subsystem refactoring, many software tests.
* Improve example programs `datasource-health-*`
* Add example program `datasource-query.py`
* Add example program `grafanalib-upload-dashboard.py`
* Fix endless-loop bug in the `search_teams` function. Thanks, @changdingfang!
* Set the `User-Agent` header to `grafana-client/{version}`
* Don't permit scalar value as JSON request body to the Grafana HTTP API,
  it is always wrong. Thanks, @ricmano!
* Example `datasource-health-check`: Without `--uid` option, scan the whole
  Grafana instance
* Data source health check: Be graceful on network read timeouts
* Data source health check: Improve acceptance criteria when probing Prometheus
* Data source health check: Clean up core implementation, add more tests
  Code coverage is now at 100%.
* Add support for "Dashboard Versions" API. Thanks, @DrMxxxxx!
* Add `datasource.query_range()` and `datasource.series()` functions
  to retrieve metric values. Thanks, @RalfHerzog!


## 2.3.0 (2022-05-26)

* Make `GrafanaApi(auth=)` an optional argument. This makes it easier to
  connect to Grafana instances that do not require authentication.
* Add basic example program, inquiring `play.grafana.org`.


## 2.2.1 (2022-05-20)

* Fix annotations query string parameter `dashboardId`. Thanks, @richbon75!


## 2.2.0 (2022-03-16)

* Retrieve dashboard by name/title. Thanks, @luixx!
* Fixed annotations tags and userid params. Thanks, @Lasica!


## 2.1.0 (2022-02-07)

* Add handler for health API. Thanks, @peekjef72!
* Add support for datasource proxying. Thanks, @peekjef72!
* Fix compatibility between `actions/checkout@v2` and `setuptools_scm`
* Fix `folderId` propagation for `update_dashboard`


## 2.0.2 (2022-02-03)

* Another release fixup, because GHA still wants to build 2.0.0.


## 2.0.1 (2022-02-03)

* Just a release fixup, because 2.0.0 has accidentally been published during testing already.


## [2.0.0](https://github.com/panodata/grafana-client/compare/1.0.3...2.0.0) (2022-02-03)

* CI: Make release job grab the complete repository history. Thanks, @m0nhawk!
* CI: Fix path to `conda/setup.py`. Thanks, @m0nhawk!
* Improve README: Add examples for creating a user and an organization.
  Thanks, @patsevanton!
* Fork the repository to https://github.com/panodata/grafana-client.
  Discussion: https://github.com/m0nhawk/grafana_api/issues/88.
* Rename Python package from `grafana_api` to `grafana-client` and
  update the repository location.
* CI: Fix tests on PyPy by installing `libxml2-dev` and `libxslt-dev`
* CI: Fix Codecov uploader by using GitHub Action recipe
* CI: Remove CodeQL analysis
* Adjust documentation to project fork
* CI: Expand test matrix by Python 3.9 and 3.10
* Add `CHANGELOG.md`, generated with `chglog`
* CI: Remove automatic changelog generation with `chglog`
* Refactoring: Rename module names and references
* Format code with `black` and `isort`
* Improve inline documentation
* Add `MANIFEST.in` to exclude specific files from `sdist` package
* CI: Update from `pep517.build` to `build`
* CI: Modernize package versions
* CI: Don't fail run when upload to Codecov fails


<a name="1.0.3"></a>
## [1.0.3](https://github.com/panodata/grafana-client/compare/1.0.2...1.0.3) (2020-08-16)

### Bug Fixes

* git history for tests (00c9331)
* add test for install (3ff0d7d)
* wrong tag for gh-action-pypi-publish (5e2bbf2)
* wrong tag for checkout action (9d20cd3)

### Features

* update (6bd5807)
* skip existing package on Test PyPi (599cdf2)
* update Conda package publish (8d19a25)
* update test workflow (088fd9d)
* updates (e3f59a2)
* add Markdown for long description (a870f80)
* move to PEP-517 (7aab182)
* run on "push" (5034f17)
* updated workflow (56f9010)
* remove poetry.lock (6c35d9b)
* update poetry.lock (ecf18f2)
* update dev packages (f330f24)
* remove setup.py (6d8c744)
* update to Poetry (a1a3f57)

### Pull Requests

* Merge pull request [#73](https://github.com/m0nhawk/grafana_api/issues/73) from m0nhawk/feat/new-workflows
* Merge pull request [#72](https://github.com/m0nhawk/grafana_api/issues/72) from m0nhawk/feat/poetry
* Merge pull request [#71](https://github.com/m0nhawk/grafana_api/issues/71) from mottish/master
* Merge pull request [#67](https://github.com/m0nhawk/grafana_api/issues/67) from Frantisek12/feat/readme


<a name="1.0.2"></a>
## [1.0.2](https://github.com/panodata/grafana-client/compare/1.0.1...1.0.2) (2020-05-18)

### Bug Fixes

* verbose output (b37fc07)
* update Github Secret name :/ (1aa3e36)
* binary name (a610d41)
* release workflow (4f64a1e)

### Pull Requests

* Merge pull request [#66](https://github.com/m0nhawk/grafana_api/issues/66) from beingnikhilarora/master
* Merge pull request [#65](https://github.com/m0nhawk/grafana_api/issues/65) from djessedirckx/feature/notifications


<a name="1.0.1"></a>
## [1.0.1](https://github.com/panodata/grafana-client/compare/1.0.0...1.0.1) (2020-03-18)

### Features

* new release pipeline (ae1bad3)

### Pull Requests

* Merge pull request [#60](https://github.com/m0nhawk/grafana_api/issues/60) from teodoryantcheff/master
* Merge pull request [#57](https://github.com/m0nhawk/grafana_api/issues/57) from m0nhawk/dependabot/pip/unittest-xml-reporting-approx-eq-3.0


<a name="1.0.0"></a>
## [1.0.0](https://github.com/panodata/grafana-client/compare/0.9.3...1.0.0) (2020-02-07)

### Features

* remove CircleCI (70994fd)
* update to Github Actions PyPa (f4f3ae1)
* Github actions tests (74b5c75)


<a name="0.9.3"></a>
## [0.9.3](https://github.com/panodata/grafana-client/compare/0.9.2...0.9.3) (2020-01-22)

### Pull Requests

* Merge pull request [#55](https://github.com/m0nhawk/grafana_api/issues/55) from megamorf/hotfix/fix_tags_parameter


<a name="0.9.2"></a>
## [0.9.2](https://github.com/panodata/grafana-client/compare/0.9.1...0.9.2) (2019-12-17)

### Pull Requests

* Merge pull request [#52](https://github.com/m0nhawk/grafana_api/issues/52) from larsderidder/improve-errors
* Merge pull request [#53](https://github.com/m0nhawk/grafana_api/issues/53) from m0nhawk/dependabot/pip/coverage-approx-eq-5.0


<a name="0.9.1"></a>
## [0.9.1](https://github.com/panodata/grafana-client/compare/0.9.0...0.9.1) (2019-10-19)

### Pull Requests

* Merge pull request [#49](https://github.com/m0nhawk/grafana_api/issues/49) from lukassup/annotation-id
* Merge pull request [#48](https://github.com/m0nhawk/grafana_api/issues/48) from lukassup/master


<a name="0.9.0"></a>
## [0.9.0](https://github.com/panodata/grafana-client/compare/0.8.6...0.9.0) (2019-09-16)


<a name="0.8.6"></a>
## [0.8.6](https://github.com/panodata/grafana-client/compare/0.8.5...0.8.6) (2019-09-16)

### Pull Requests

* Merge pull request [#46](https://github.com/m0nhawk/grafana_api/issues/46) from Sytten/master


<a name="0.8.5"></a>
## [0.8.5](https://github.com/panodata/grafana-client/compare/0.8.4...0.8.5) (2019-09-09)

### Pull Requests

* Merge pull request [#43](https://github.com/m0nhawk/grafana_api/issues/43) from Sytten/master
* Merge pull request [#41](https://github.com/m0nhawk/grafana_api/issues/41) from m0nhawk/dependabot/pip/requests-mock-approx-eq-1.7


<a name="0.8.4"></a>
## [0.8.4](https://github.com/panodata/grafana-client/compare/v0.5.3...0.8.4) (2019-08-19)

### Bug Fixes

* **README:** remove coveralls badge (f36e976)
* **api:** python2 Teams support, fix [#24](https://github.com/m0nhawk/grafana_api/issues/24) (c8cfd37)
* **circleci:** do not put VERSION file to Github release (59d3e7d)
* **organization:** fix [#11](https://github.com/m0nhawk/grafana_api/issues/11), rename to “Organization” the same as in Grafana API (d445d91)
* **python:** error handling which doesn't hide exceptions, addresses [#37](https://github.com/m0nhawk/grafana_api/issues/37) (ba76dc6)

### Features

* **auto-deploy:** build package automatically (5b16e31)
* **circleci:** test on Python 2.7, 3.6 & 3.7 (3906264)
* **circleci:** remove debug statements (a4c29f8)
* **circleci:** pre-create git version (27fac5a)
* **dep:** adding missing dependency for Python 2 testing (d1324ad)
* **travis:** remove (a4f65ae)

### Pull Requests

* Merge pull request [#39](https://github.com/m0nhawk/grafana_api/issues/39) from m0nhawk/error-handling
* Merge pull request [#36](https://github.com/m0nhawk/grafana_api/issues/36) from m0nhawk/chore/migrating-to-yaml-syntax
* Merge pull request [#35](https://github.com/m0nhawk/grafana_api/issues/35) from Panchorn/master
* Merge pull request [#33](https://github.com/m0nhawk/grafana_api/issues/33) from ohmrefresh/master
* Merge pull request [#31](https://github.com/m0nhawk/grafana_api/issues/31) from m0nhawk/feat/circleci
* Merge pull request [#30](https://github.com/m0nhawk/grafana_api/issues/30) from mbovo/issue/29
* Merge pull request [#1](https://github.com/m0nhawk/grafana_api/issues/1) from m0nhawk/master
* Merge pull request [#28](https://github.com/m0nhawk/grafana_api/issues/28) from m0nhawk/fix/python2
* Merge pull request [#27](https://github.com/m0nhawk/grafana_api/issues/27) from mbovo/issue/26
* Merge pull request [#25](https://github.com/m0nhawk/grafana_api/issues/25) from m0nhawk/dependabot/pip/requests-2.22.0
* Merge pull request [#23](https://github.com/m0nhawk/grafana_api/issues/23) from sedan07/adding-teams-support
* Merge pull request [#22](https://github.com/m0nhawk/grafana_api/issues/22) from OlegKorchagin/backward-compatibility-with-python2.7
* Merge pull request [#21](https://github.com/m0nhawk/grafana_api/issues/21) from ZubAnt/master
* Merge pull request [#20](https://github.com/m0nhawk/grafana_api/issues/20) from m0nhawk/fix/readme
* Merge pull request [#19](https://github.com/m0nhawk/grafana_api/issues/19) from m0nhawk/feat/auto-deploy
* Merge pull request [#18](https://github.com/m0nhawk/grafana_api/issues/18) from m0nhawk/fix/organization



<a name="0.8.3"></a>
## [0.8.3](https://github.com/panodata/grafana-client/compare/0.8.2...0.8.3) (2019-08-08)

### Pull Requests

* Merge pull request [#35](https://github.com/m0nhawk/grafana_api/issues/35) from Panchorn/master


<a name="0.8.2"></a>
## [0.8.2](https://github.com/panodata/grafana-client/compare/0.8.1...0.8.2) (2019-07-23)


<a name="0.8.1"></a>
## [0.8.1](https://github.com/panodata/grafana-client/compare/0.8.0...0.8.1) (2019-07-20)


<a name="0.8.0"></a>
## [0.8.0](https://github.com/panodata/grafana-client/compare/0.7.5...0.8.0) (2019-07-20)

### Features

* **circleci:** test on Python 2.7, 3.6 & 3.7 (3906264)
* **dep:** adding missing dependency for Python 2 testing (d1324ad)
* **travis:** remove (a4f65ae)

### Pull Requests

* Merge pull request [#33](https://github.com/m0nhawk/grafana_api/issues/33) from ohmrefresh/master
* Merge pull request [#31](https://github.com/m0nhawk/grafana_api/issues/31) from m0nhawk/feat/circleci


<a name="0.7.5"></a>
## [0.7.5](https://github.com/panodata/grafana-client/compare/0.7.4...0.7.5) (2019-06-06)

### Pull Requests

* Merge pull request [#30](https://github.com/m0nhawk/grafana_api/issues/30) from mbovo/issue/29
* Merge pull request [#1](https://github.com/m0nhawk/grafana_api/issues/1) from m0nhawk/master


<a name="0.7.4"></a>
## [0.7.4](https://github.com/panodata/grafana-client/compare/0.7.3...0.7.4) (2019-06-05)

### Bug Fixes

* **api:** python2 Teams support, fix [#24](https://github.com/m0nhawk/grafana_api/issues/24) (c8cfd37)

### Pull Requests

* Merge pull request [#28](https://github.com/m0nhawk/grafana_api/issues/28) from m0nhawk/fix/python2
* Merge pull request [#27](https://github.com/m0nhawk/grafana_api/issues/27) from mbovo/issue/26
* Merge pull request [#25](https://github.com/m0nhawk/grafana_api/issues/25) from m0nhawk/dependabot/pip/requests-2.22.0


<a name="0.7.3"></a>
## [0.7.3](https://github.com/panodata/grafana-client/compare/0.7.2...0.7.3) (2019-05-04)

### Pull Requests

* Merge pull request [#23](https://github.com/m0nhawk/grafana_api/issues/23) from sedan07/adding-teams-support


<a name="0.7.2"></a>
## [0.7.2](https://github.com/panodata/grafana-client/compare/0.7.1...0.7.2) (2019-04-28)

### Pull Requests

* Merge pull request [#22](https://github.com/m0nhawk/grafana_api/issues/22) from OlegKorchagin/backward-compatibility-with-python2.7


<a name="0.7.1"></a>
## [0.7.1](https://github.com/panodata/grafana-client/compare/0.7.0...0.7.1) (2019-04-22)

### Bug Fixes

* **README:** remove coveralls badge (f36e976)
* **circleci:** do not put VERSION file to Github release (59d3e7d)

### Features

* **circleci:** remove debug statements (a4c29f8)

### Pull Requests

* Merge pull request [#21](https://github.com/m0nhawk/grafana_api/issues/21) from ZubAnt/master
* Merge pull request [#20](https://github.com/m0nhawk/grafana_api/issues/20) from m0nhawk/fix/readme


<a name="0.7.0"></a>
## [0.7.0](https://github.com/panodata/grafana-client/compare/0.6.0...0.7.0) (2019-04-05)

### Bug Fixes

* **organization:** fix [#11](https://github.com/m0nhawk/grafana_api/issues/11), rename to “Organization” the same as in Grafana API (d445d91)

### Features

* **auto-deploy:** build package automatically (5b16e31)
* **circleci:** pre-create git version (27fac5a)

### Pull Requests

* Merge pull request [#19](https://github.com/m0nhawk/grafana_api/issues/19) from m0nhawk/feat/auto-deploy
* Merge pull request [#18](https://github.com/m0nhawk/grafana_api/issues/18) from m0nhawk/fix/organization


<a name="0.6.0"></a>
## [0.6.0](https://github.com/panodata/grafana-client/compare/v0.5.2...0.6.0) (2019-03-31)

### Features

* **deploy:** setup Github actions for deployment (76de1bf)
* **test:** store Artifacts (1c67dd5)
* **test:** JUnit reporting for CircleCI (79b8063)

### Pull Requests

* Merge pull request [#16](https://github.com/m0nhawk/grafana_api/issues/16) from m0nhawk/test/codecov
* Merge pull request [#15](https://github.com/m0nhawk/grafana_api/issues/15) from m0nhawk/test/coverage
* Merge pull request [#13](https://github.com/m0nhawk/grafana_api/issues/13) from m0nhawk/feat/test
* Merge pull request [#12](https://github.com/m0nhawk/grafana_api/issues/12) from max-rocket-internet/actual_quickstart


<a name="v0.5.3"></a>
## [v0.5.3](https://github.com/panodata/grafana-client/compare/v0.5.2...v0.5.3) (2019-08-19)

### Features

* **deploy:** setup Github actions for deployment (76de1bf)
* **test:** store Artifacts (1c67dd5)
* **test:** JUnit reporting for CircleCI (79b8063)
* **tests:** improve coverage for SonarCloud (4701c1c)

### Pull Requests

* Merge pull request [#16](https://github.com/m0nhawk/grafana_api/issues/16) from m0nhawk/test/codecov
* Merge pull request [#15](https://github.com/m0nhawk/grafana_api/issues/15) from m0nhawk/test/coverage
* Merge pull request [#13](https://github.com/m0nhawk/grafana_api/issues/13) from m0nhawk/feat/test
* Merge pull request [#12](https://github.com/m0nhawk/grafana_api/issues/12) from max-rocket-internet/actual_quickstart
* Merge pull request [#10](https://github.com/m0nhawk/grafana_api/issues/10) from marfx000/tag-filter-fix
* Merge pull request [#9](https://github.com/m0nhawk/grafana_api/issues/9) from Eric-Fontana-Bose/master
* Merge pull request [#8](https://github.com/m0nhawk/grafana_api/issues/8) from asalkeld/fix-tests
* Merge pull request [#6](https://github.com/m0nhawk/grafana_api/issues/6) from asalkeld/fix-token-auth
* Merge pull request [#7](https://github.com/m0nhawk/grafana_api/issues/7) from asalkeld/support-ssl-noverify


<a name="v0.5.2"></a>
## [v0.5.2](https://github.com/panodata/grafana-client/compare/v0.5.1...v0.5.2) (2019-02-26)


<a name="v0.5.1"></a>
## [v0.5.1](https://github.com/panodata/grafana-client/compare/v0.5.0...v0.5.1) (2019-02-04)

### Pull Requests

* Merge pull request [#10](https://github.com/m0nhawk/grafana_api/issues/10) from marfx000/tag-filter-fix


<a name="v0.5.0"></a>
## [v0.5.0](https://github.com/panodata/grafana-client/compare/v0.3.5...v0.5.0) (2018-11-25)

### Pull Requests

* Merge pull request [#9](https://github.com/m0nhawk/grafana_api/issues/9) from Eric-Fontana-Bose/master


<a name="v0.3.6"></a>
## v0.3.6 (2018-11-04)

### Features

* **tests:** improve coverage for SonarCloud (4701c1c)

### Pull Requests

* Merge pull request [#9](https://github.com/m0nhawk/grafana_api/issues/9) from Eric-Fontana-Bose/master
* Merge pull request [#8](https://github.com/m0nhawk/grafana_api/issues/8) from asalkeld/fix-tests
* Merge pull request [#6](https://github.com/m0nhawk/grafana_api/issues/6) from asalkeld/fix-token-auth
* Merge pull request [#7](https://github.com/m0nhawk/grafana_api/issues/7) from asalkeld/support-ssl-noverify
* Merge pull request [#4](https://github.com/m0nhawk/grafana_api/issues/4) from svet-b/fix_setup
* Merge pull request [#3](https://github.com/m0nhawk/grafana_api/issues/3) from tharvik/master
* Merge pull request [#2](https://github.com/m0nhawk/grafana_api/issues/2) from cristim/master
* Merge pull request [#1](https://github.com/m0nhawk/grafana_api/issues/1) from tescalada/master


<a name="v0.3.5"></a>
## [v0.3.5](https://github.com/panodata/grafana-client/compare/v0.3.4...v0.3.5) (2018-10-17)

### Pull Requests

* Merge pull request [#8](https://github.com/m0nhawk/grafana_api/issues/8) from asalkeld/fix-tests


<a name="v0.3.4"></a>
## [v0.3.4](https://github.com/panodata/grafana-client/compare/v0.3.3...v0.3.4) (2018-10-17)

### Pull Requests

* Merge pull request [#6](https://github.com/m0nhawk/grafana_api/issues/6) from asalkeld/fix-token-auth
* Merge pull request [#7](https://github.com/m0nhawk/grafana_api/issues/7) from asalkeld/support-ssl-noverify


<a name="v0.3.3"></a>
## [v0.3.3](https://github.com/panodata/grafana-client/compare/v0.3.1...v0.3.3) (2018-10-10)

### Features

* **tests:** improve coverage for SonarCloud (4701c1c)

### Pull Requests

* Merge pull request [#4](https://github.com/m0nhawk/grafana_api/issues/4) from svet-b/fix_setup


<a name="v0.3.2"></a>
## [v0.3.2](https://github.com/panodata/grafana-client/compare/v0.2.7...v0.3.2) (2018-10-07)

### Pull Requests

* Merge pull request [#4](https://github.com/m0nhawk/grafana_api/issues/4) from svet-b/fix_setup
* Merge pull request [#3](https://github.com/m0nhawk/grafana_api/issues/3) from tharvik/master


<a name="v0.3.1"></a>
## [v0.3.1](https://github.com/panodata/grafana-client/compare/v0.3.0...v0.3.1) (2018-10-05)


<a name="v0.3.0"></a>
## [v0.3.0](https://github.com/panodata/grafana-client/compare/v0.2.9...v0.3.0) (2018-10-04)


<a name="v0.2.9"></a>
## [v0.2.9](https://github.com/panodata/grafana-client/compare/v0.2.8...v0.2.9) (2018-10-04)


<a name="v0.2.8"></a>
## [v0.2.8](https://github.com/panodata/grafana-client/compare/v0.2.6...v0.2.8) (2018-06-03)

### Pull Requests

* Merge pull request [#3](https://github.com/m0nhawk/grafana_api/issues/3) from tharvik/master
* Merge pull request [#2](https://github.com/m0nhawk/grafana_api/issues/2) from cristim/master
* Merge pull request [#1](https://github.com/m0nhawk/grafana_api/issues/1) from tescalada/master


<a name="v0.2.7"></a>
## [v0.2.7](https://github.com/panodata/grafana-client/compare/v0.1.1...v0.2.7) (2018-04-19)

### Pull Requests

* Merge pull request [#2](https://github.com/m0nhawk/grafana_api/issues/2) from cristim/master
* Merge pull request [#1](https://github.com/m0nhawk/grafana_api/issues/1) from tescalada/master


<a name="v0.2.6"></a>
## [v0.2.6](https://github.com/panodata/grafana-client/compare/v0.2.2...v0.2.6) (2018-03-17)


<a name="v0.2.2"></a>
## [v0.2.2](https://github.com/panodata/grafana-client/compare/v0.2.1...v0.2.2) (2018-01-12)


<a name="v0.2.1"></a>
## [v0.2.1](https://github.com/panodata/grafana-client/compare/v0.2.0...v0.2.1) (2018-01-12)


<a name="v0.2.0"></a>
## [v0.2.0](https://github.com/panodata/grafana-client/compare/v0.1.7...v0.2.0) (2018-01-10)


<a name="v0.1.7"></a>
## [v0.1.7](https://github.com/panodata/grafana-client/compare/v0.1.6...v0.1.7) (2018-01-10)


<a name="v0.1.6"></a>
## [v0.1.6](https://github.com/panodata/grafana-client/compare/v0.1.5...v0.1.6) (2017-12-29)


<a name="v0.1.5"></a>
## [v0.1.5](https://github.com/panodata/grafana-client/compare/v0.1.4...v0.1.5) (2017-12-21)


<a name="v0.1.4"></a>
## [v0.1.4](https://github.com/panodata/grafana-client/compare/v0.1.3...v0.1.4) (2017-12-19)


<a name="v0.1.3"></a>
## [v0.1.3](https://github.com/panodata/grafana-client/compare/v0.1.2...v0.1.3) (2017-12-17)


<a name="v0.1.2"></a>
## [v0.1.2](https://github.com/panodata/grafana-client/compare/v0.1.1...v0.1.2) (2017-12-06)


<a name="v0.1.1"></a>
## [v0.1.1](https://github.com/panodata/grafana-client/compare/v0.1.0...) (2017-12-06)
