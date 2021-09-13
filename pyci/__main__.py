import argparse
import importlib
import logging

from pyci import __version__
from .config.logging import (
    handler_stdout,
    handler_file,
    formatter_default,
    formatter_iso6801,
    filter_passwords
)

LOG = logging.getLogger(__name__)

try:
    importlib.import_module("paho.mqtt.client")
except ModuleNotFoundError:
    mqtt = False
    pass


def main():
    global mqtt

    print("hello")
    parser = argparse.ArgumentParser()

    # _standard_ parsing arguments
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__
    )
    parser.add_argument(
        "--logfile",
        default="stdout",
        help="File where logs are to be written"
    )

    bus_parser = parser.add_subparsers(help="bus", dest="bus")
    bus_parser.required = True

    unix_domain_socket_bus = bus_parser.add_parser(
        "ipc",
        help="Unix Inter-Process-Communication Socket."
    )
    unix_domain_socket_bus.add_argument("--socket", default="/tmp/pyci_socket")
    # unix_domain_socket_bus.add_argument("--notification-socket", default="/tmp/pyci_notify_socket")

    if mqtt:
        mqtt_bus = bus_parser.add_parser(
            "mqtt",
            help="MQTT Bus"
        )
        mqtt_bus.add_argument("--server", default="0.0.0.0")
        mqtt_bus.add_argument("--port", default="1883")

    args = parser.parse_args()

    # configure logger
    verbosity_levels = {
        0: logging.ERROR,
        1: logging.WARN,
        2: logging.INFO,
        3: logging.DEBUG
    }

    LOG.setLevel(logging.DEBUG)

    verbosity_level = verbosity_levels.get(args.verbose, logging.DEBUG)
    if args.logfile:
        handler_file.setLevel(verbosity_level)
        handler_file.setFormatter(formatter_iso6801)
        handler_file.addFilter(filter_passwords)
        LOG.addHandler(handler_file)
    else:
        handler_stdout.setLevel(verbosity_level)
        handler_stdout.setFormatter(formatter_default)
        LOG.addHandler(handler_stdout)

    LOG.info("Starting PyCI version {version}".format(version=__version__))

    buses = {
        "ipc": init_unix_ipc_bus,
        "mqtt": init_mqtt_bus
    }
    print(buses)


def init_bus_not_implemented(args: dict):
    raise NotImplementedError(
        "{bus} is not implemented".format(bus=args.backend)
    )


def init_unix_ipc_bus():
    LOG.info("Selected Bus: UNIX Socket (IPC).")
    from pyci.bus.ipc import UnixSocketListener, UnixSocketSender
    print(UnixSocketListener, UnixSocketSender)


def init_mqtt_bus():
    LOG.info("Selected Bus: MQTT.")
    from pyci.bus.mqtt import MqttListener, MqttSender
    print(MqttListener, MqttSender)


if __name__ == "__main__":
    main()
