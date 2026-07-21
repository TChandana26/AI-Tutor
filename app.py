from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from data_structures import PDFDocument, ChatSession, AIRequest
from pdf_reader import extract_text
from ai_engine import get_answer
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs('uploads', exist_ok=True)

# In-memory session store  { session_id: ChatSession }
sessions = {}

# ── Route 1: Serve UI ─────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

# ── Route 2: Upload PDF ───────────────────────────
@app.route('/upload', methods=['POST'])
def upload_pdf():
    file = request.files.get('pdf')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        text, pages = extract_text(filepath)
    except ValueError as e:
        os.remove(filepath)  # delete the unusable file
        return jsonify({'error': str(e)}), 422

    doc = PDFDocument(filename=filename, filepath=filepath,
                      text_content=text, pages=pages)
    session = ChatSession(document=doc)
    sessions[session.session_id] = session

    return jsonify({
        'session_id': session.session_id,
        'filename':   doc.filename,
        'pages':      doc.pages,
        'message':    'PDF uploaded successfully!'
    })

# ── Route 3: Ask a Question ───────────────────────
@app.route('/ask', methods=['POST'])
def ask_question():
    data       = request.get_json()
    session_id = data.get('session_id')
    question   = data.get('question')

    session = sessions.get(session_id)
    if not session:
        return jsonify({'error': 'Session not found'}), 404

    session.add_message('user', question)

    ai_req = AIRequest(question=question,
                       context=session.document.text_content)
    answer = get_answer(ai_req)

    session.add_message('assistant', answer)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)