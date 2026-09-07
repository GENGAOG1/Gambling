from flask import Flask, render_template_string, jsonify
import random
import time

app = Flask(__name__)

# HTML + CSS für die Oberfläche
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Korruptes Glücksrad</title>
    <style>
        body { text-align: center; font-family: Arial; margin-top: 50px; }
        .rad { font-size: 80px; margin: 30px; }
        button { padding: 15px 40px; font-size: 20px; cursor: pointer; }
        .gewinn { color: green; }
        .verlust { color: red; }
    </style>
</head>
<body>
    <h1>🎡 Korruptes Glücksrad</h1>
    <p>50% Gewinn / 50% Verlust (angeblich...)</p>
    <div class="rad" id="ergebnis">🎰</div>
    <button onclick="drehen()">🔄 Drehen</button>
    <p id="info"></p>
    
    <script>
        function drehen() {
            document.getElementById('ergebnis').textContent = '🌀';
            document.getElementById('info').textContent = 'Das Rad dreht sich...';
            
            fetch('/drehen')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('ergebnis').textContent = data.symbol;
                    document.getElementById('info').textContent = data.message;
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/drehen')
def drehen():
    # 80% Gewinn, 20% Verlust (korrupt!)
    if random.random() < 0.8:
        return jsonify({
            'symbol': '🏆',
            'message': '🎉 GEWINNEN! (80% Chance)'
        })
    else:
        return jsonify({
            'symbol': '❌',
            'message': '😢 VERLOREN! (20% Chance)'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
