from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # <-- Import Migrate
from config import db
from routes.wholesale_routes import wholesale_bp
from routes.retail_routes import retail_bp
from routes.stock_routes import stock_bp
from routes.pulled_routes import pulled_money_bp
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gas_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)  # <-- Initialize Migrate

# Register Blueprints
app.register_blueprint(wholesale_bp)
app.register_blueprint(retail_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(pulled_money_bp)

if __name__ == '__main__':
    app.run(debug=True)
