import logging

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

# SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

with app.app_context():
    db.create_all()
    logger.info("Database initialized successfully")

@app.route("/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    logger.info("Fetching all items")
    return jsonify([item.to_dict() for item in items])


@app.route("/items", methods=["POST"])
def create_item():
    try:
        data = request.get_json()

        if not data or "name" not in data:
            return jsonify({"error": "Invalid input"}), 400

        new_item = Item(name=data["name"])

        db.session.add(new_item)
        db.session.commit()

        #Logging the creation of a new item
        logger.info(f"Created new item with ID: {new_item.id} and Name: {new_item.name}")

        return jsonify(new_item.to_dict()), 201

    except SQLAlchemyError:
        db.session.rollback()
        logger.error("Database error occurred while creating an item", exc_info=True)
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        logger.error("An unexpected error occurred", exc_info=True)
        return jsonify({"error": str(e)}), 500
    

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    try:
        item = Item.query.get(item_id)

        if not item:
            return jsonify({"error": "Item not found"}), 404

        data = request.get_json()

        if not data or "name" not in data:
            return jsonify({"error": "Invalid input"}), 400

        item.name = data["name"]
        db.session.commit()

        return jsonify(item.to_dict()), 200

    except SQLAlchemyError:
        db.session.rollback()
        logger.error("Database error occurred while updating an item", exc_info=True)
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        logger.error("An unexpected error occurred", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    try:
        item = Item.query.get(item_id)

        if not item:
            return jsonify({"error": "Item not found"}), 404

        db.session.delete(item)
        db.session.commit()

        return jsonify({"message": "Item deleted successfully"}), 200

    except SQLAlchemyError:
        db.session.rollback()
        logger.error("Database error occurred while deleting an item", exc_info=True)
        return jsonify({"error": "Database error"}), 500

    except Exception as e:
        logger.error("An unexpected error occurred", exc_info=True)
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)