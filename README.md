# yoda-web-mock

This repository contains a Flask project that can mock various web applications
that Yoda depends on. It is intended to be used for development and testing
purposes.

## Running a mocked service

The web mock service would usually be installed using the Yoda Ansible playbook.

If you want to run a mocked service locally, you can run Flask in development mode.
The mock type is configured using the `MOCK_TYPE` environment variable, like so:

```
MOCK_TYPE="datacite" FLASK_APP="yoda_web_mock/app.py" python3 -m flask run
```

## Currently available mocks

* Datacite (used by Yoda during the publication process, e.g. to register a DOI persistent identifier)
* SRAM (SURF Research Access Management, provides services related to authentication and authorization)

## Bug reports
We use GitHub for bug tracking.
Please search existing [issues](https://github.com/UtrechtUniversity/yoda/issues) and create a new one if the issue is not yet tracked.

## Questions and ideas
The best place to reach us about questions and ideas regarding Yoda is on our [GitHub Discussions page](https://github.com/utrechtuniversity/yoda/discussions).

## License
This project is licensed under the GPL-v3 license.
The full license can be found in [LICENSE](LICENSE).
