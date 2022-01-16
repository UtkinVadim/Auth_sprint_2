from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

import config

trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: config.SERVICE_NAME_IN_JAEGER})
    )
)

jaeger_exporter = JaegerExporter(
    agent_host_name=config.JAEGER_HOST,
    agent_port=config.JAEGER_PORT,
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)


def add_tracer(app):
    """
    Добавляет трассировку flask приложения в jaeger
    Результат можно посмотреть по ссылке:
    http://${JAEGER_HOST}:16686/

    :param app:
    :return:
    """
    FlaskInstrumentor().instrument_app(app, excluded_urls=config.JAEGER_EXCLUDED_URLS)
