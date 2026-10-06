# routes/water_refilling.py
from flask import Blueprint
from controllers.water_refilling_controller import *

wr_bp = Blueprint('water_refilling', __name__, url_prefix='/api/water-refilling')

wr_bp.route('/customers', methods=['GET'])(get_customers)
wr_bp.route('/orders', methods=['POST'])(create_order)
# …remaining endpoints
