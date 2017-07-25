import argparse
import sys
import signal

from chaussette.server import make_server
from werkzeug.serving import run_with_reloader

from runnerly.dataservice.app import create_app
from runnerly.dataservice.database import db, init_database


def _quit(signal, frame):
    print("Bye!")
    # add any cleanup code here
    sys.exit(0)


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Runnerly Dataservice')

    parser.add_argument('--fd', type=int, default=None)
    parser.add_argument('--config-file', help='Config file',
                        type=str, default=None)
    args = parser.parse_args(args=args)

    app = create_app(args.config_file)
    host = app.config.get('host', '0.0.0.0')
    port = app.config.get('port', 5000)
    debug = app.config.get('DEBUG', False)

    signal.signal(signal.SIGINT, _quit)
    signal.signal(signal.SIGTERM, _quit)

    db.init_app(app)
    db.app = app
    db.create_all(app=app)
    init_database()

    if args.fd is not None:
        # use chaussette
        httpd = make_server(app, host='fd://%d' % args.fd)
        httpd.serve_forever()
    else:
        app.run(debug=debug, host=host, port=port, use_reloader=debug)


if __name__ == "__main__":
    main()
