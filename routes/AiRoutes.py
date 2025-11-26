from flask import Blueprint, jsonify
from bot.jhpiego_bot import jhpiego_bot

ai_bp = Blueprint('ai_bp', __name__)

@ai_bp.route('/ai/faq', methods=['GET'])
def get_faq():
    faq = jhpiego_bot.generate_faq()
    if not faq:
        return jsonify({"faq": [], "message": "Nenhuma pergunta frequente encontrada"}), 200
    
    return jsonify({"faq": faq}), 200
