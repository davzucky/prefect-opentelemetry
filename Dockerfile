FROM python:3.10-slim AS python-builder

WORKDIR /src
COPY . ./

RUN python -m pip install --upgrade pip build && \
    python -m pip install --upgrade --upgrade-strategy eager -e .[dev] && \
    python -m build --sdist --wheel --outdir /src/dist/ 

# RUN ls /src/dist/ 
# RUN mv "/src/dist/$(python setup.py --fullname | sed -e '0,/-/ s/-/_/' )-py3-none-any.whl" "/src/dist/"


FROM python:3.10-slim AS final

WORKDIR /opt/prefect

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

COPY --from=python-builder /src/dist/*.whl ./dist/

RUN pip install --no-cache-dir $(ls ./dist/*.whl)

# prefect-opentelemetry-0+unknown-py3-none-any.whl
# prefect_opentelemetry-0+unknown-py3-none-any.whl

# prefect_opentelemetry-0+unknown-py3-none-any.whl
# prefect-opentelemetry-0+unknown-py3-none-any.whl

# mv "dist/$(python setup.py --fullname | sed -e '0,/-/ s/-/_/' )-py3-none-any.whl" "dist/prefect_opentelemetry-py3-none-any.whl"

# python -m build --sdist --wheel --outdir dist/ 

# prefect-opentelemetry-0+untagged.40.ge5910d2-py3-none-any.whl
# prefect_opentelemetry-0+untagged.40.ge5910d2-py3-none-any.whl
