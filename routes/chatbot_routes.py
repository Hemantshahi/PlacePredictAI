"""
routes/chatbot_routes.py — AI Chatbot Routes (Gemini API)
MCE Placement Prediction System
"""
import os
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user

chatbot_bp = Blueprint('chatbot', __name__)

SYSTEM_PROMPT = """You are PlaceBot, an intelligent AI assistant for Motihari College of Engineering (MCE), Motihari, Bihar, India.
You are part of the PlacePredict AI system built for the Training & Placement Cell of MCE.

Your introduction (when asked who you are):
"Hi! I'm PlaceBot, the AI-powered placement assistant of Motihari College of Engineering. I'm here to help you with placement preparation, career guidance, resume tips, and much more!"

Core expertise:
- Placement preparation and career guidance for engineering students
- Resume building and ATS optimization
- Technical interview preparation (DSA, System Design, OOP, DBMS, OS, CN)
- Company-specific preparation (TCS, Infosys, Wipro, Cognizant, Accenture, Google, Amazon, etc.)
- Skill development roadmaps
- Higher education guidance (GATE, MBA, MS abroad)
- Soft skills and communication
- Job market trends for freshers in India
- General knowledge and any topic a student might ask

Important rules:
- ALWAYS reply in English only — never use Hindi or Hinglish
- Be friendly, encouraging, and professional
- Give specific, actionable, practical advice
- You can answer ANY question — not just placement related
- Always end with an actionable tip or next step
- When greeting for the first time, introduce yourself as PlaceBot
- Keep responses concise but complete
"""


@chatbot_bp.route('/')
@login_required
def chatbot_page():
    from models.models import ChatHistory
    history = ChatHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(ChatHistory.timestamp.asc()).limit(20).all()
    return render_template('chatbot/chat.html', history=history)


@chatbot_bp.route('/message', methods=['POST'])
@login_required
def send_message():
    from app import db
    from models.models import ChatHistory

    data = request.get_json()
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    # Save user message
    user_chat = ChatHistory(
        user_id=current_user.id,
        role='user',
        message=user_message
    )
    db.session.add(user_chat)

    # Chat history for context
    history = ChatHistory.query.filter_by(
        user_id=current_user.id
    ).order_by(ChatHistory.timestamp.asc()).limit(10).all()

    try:
        import google.generativeai as genai

        api_key = os.environ.get('GEMINI_API_KEY', '')
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=SYSTEM_PROMPT
        )

        # Build chat history
        chat_history = []
        for h in history:
            role = 'user' if h.role == 'user' else 'model'
            chat_history.append({
                'role': role,
                'parts': [h.message]
            })

        chat = model.start_chat(history=chat_history)
        response = chat.send_message(user_message)
        bot_reply = response.text

    except Exception as e:
        print(f"Gemini API Error: {e}")
        bot_reply = (
            "I apologize, I'm having trouble connecting right now. "
            "Please try again in a moment."
        )

    # Save bot response
    bot_chat = ChatHistory(
        user_id=current_user.id,
        role='assistant',
        message=bot_reply
    )
    db.session.add(bot_chat)
    db.session.commit()

    return jsonify({'reply': bot_reply})


@chatbot_bp.route('/clear', methods=['POST'])
@login_required
def clear_chat():
    from app import db
    from models.models import ChatHistory
    ChatHistory.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({'status': 'cleared'})