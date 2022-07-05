"""
Defines the Orion FastAPI app on which we enable opentelemetry
"""
from fastapi import FastAPI
from prefect.orion.api.server import create_app
from prefect.settings import Settings


def create_prefect_with_opentelemetry(
    settings: Settings = None,
    ephemeral: bool = False,
    ignore_cache: bool = False,
) -> FastAPI:
    """
    Create an FastAPI app with opentelemtry enable that includes the Orion API and UI

    Args:
        settings: The settings to use to create the app. If not set, settings are pulled
            from the context.
        ignore_cache: If set, a new application will be created even if the settings
            match. Otherwise, an application is returned from the cache.
        ephemeral: If set, the application will be treated as ephemeral. The UI
            and services will be disabled.
    """

    app = create_app(settings=settings, ephemeral=ephemeral, ignore_cache=ignore_cache)

    # provider = TracerProvider(
    #     resource=Resource.create(
    #         {
    #             "service.name": "Prefect",
    #             "service.version": prefect.__version__,
    #             "process.runtime.name": sys.implementation.name,
    #             "process.runtime.version": sys.implementation.version,
    #         },
    #     ),
    # )

    return app
