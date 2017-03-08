from flakon import create_app
from dataservice.views import blueprints
from dataservice.database import db


app = create_app(blueprints=blueprints)


if __name__ == '__main__':
    db.init_app(app)
    db.create_all(app=app)
    app.run()
