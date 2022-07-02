# prefect-opentelemetry

## Welcome!

Extend prefect Orion with [Opentelemetry](https://opentelemetry.io/) capability to monitor the server side

## Getting Started

This project create a new Perfect orion factory that wrap the original one and add opentelemetry capability for the following area

- FastAPI
- SQLAlchemy
- Postgres
- SQLLite

This is setup to only export all the opentelemetry at the format OTLP to an exporter that you can use after to dispatch to your metrics, log or trace.

### Python setup

Requires an installation of Python 3.7+.

We recommend using a Python virtual environment manager such as pipenv, conda or virtualenv.

These tasks are designed to work with Prefect 2.0. For more information about how to use Prefect, please refer to the [Prefect documentation](https://orion-docs.prefect.io/).


<!-- 
No pushed yet to pypi
### Installation

Install `prefect-opentelemetry` with `pip`:

```bash
pip install prefect-opentelemetry
``` -->


## Resources

If you encounter any bugs while using `prefect-opentelemetry`, feel free to open an issue in the [prefect-opentelemetry](https://github.com/davzucky/prefect-opentelemetry) repository.

If you have any questions or issues while using `prefect-opentelemetry`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).

## Development

If you'd like to install a version of `prefect-opentelemetry` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/davzucky/prefect-opentelemetry.git

cd prefect-opentelemetry/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
