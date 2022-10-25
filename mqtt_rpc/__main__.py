import argparse

from . import mqtt_rpc, worker


def main() -> None:
    arg_parser = argparse.ArgumentParser("MQTT-RPC")
    arg_parser.add_argument("--app")

    sub_parsers = arg_parser.add_subparsers(dest="command")

    worker_parser = sub_parsers.add_parser("worker")
    worker_parser.add_argument("--concurrency", type=int)
    worker_parser.add_argument("--topic", default="all")

    args = arg_parser.parse_args()

    app = mqtt_rpc.get_app(args.app)
    app.load_imports()

    if args.command == "worker":
        worker.main(app, args.topic, args.concurrency)


if __name__ == "__main__":
    main()
