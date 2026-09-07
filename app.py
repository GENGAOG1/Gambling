from flask import Flask, render_template_string, jsonify
import random

app = Flask(__name__)

# HTML + CSS + JavaScript für das Glücksrad
HTML = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎡 Glücksrad</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        .container {
            text-align: center;
            padding: 20px;
        }
        h1 {
            color: #fff;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        }
        .subtitle {
            color: #aaa;
            font-size: 1.1em;
            margin-bottom: 30px;
        }
        .wheel-container {
            position: relative;
            display: inline-block;
            margin: 20px 0;
        }
        canvas {
            border-radius: 50%;
            box-shadow: 0 0 50px rgba(255, 215, 0, 0.2), 0 0 100px rgba(255, 215, 0, 0.1);
            cursor: pointer;
            transition: transform 0.1s;
        }
        canvas:hover {
            transform: scale(1.02);
        }
        .pointer {
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 40px;
            filter: drop-shadow(0 0 10px rgba(255, 0, 0, 0.5));
            z-index: 10;
        }
        #spinBtn {
            margin-top: 30px;
            padding: 15px 50px;
            font-size: 1.3em;
            font-weight: bold;
            background: linear-gradient(135deg, #f7971e, #ffd200);
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 5px 25px rgba(255, 215, 0, 0.4);
            color: #1a1a2e;
        }
        #spinBtn:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 35px rgba(255, 215, 0, 0.6);
        }
        #spinBtn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        #result {
            margin-top: 25px;
            font-size: 2em;
            font-weight: bold;
            color: #fff;
            min-height: 60px;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
        }
        .stats {
            margin-top: 20px;
            color: #aaa;
            font-size: 0.9em;
        }
        .stats span {
            color: #fff;
            font-weight: bold;
        }
        .gewinn { color: #00ff88; }
        .verlust { color: #ff4444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎡 Glücksrad</h1>
        <p class="subtitle">50% Gewinn / 50% Verlust </p>
        
        <div class="wheel-container">
            <div class="pointer">▼</div>
            <canvas id="wheelCanvas" width="400" height="400"></canvas>
        </div>
        
        <button id="spinBtn">🔄 DREHEN</button>
        <div id="result">🎰 Klick zum Drehen!</div>
        <div class="stats">
            Gewinne: <span id="wins" class="gewinn">0</span> &nbsp;|&nbsp; 
            Verluste: <span id="losses" class="verlust">0</span> &nbsp;|&nbsp;
            Quote: <span id="quote">0.0</span>%
        </div>
    </div>

    <script>
        const canvas = document.getElementById('wheelCanvas');
        const ctx = canvas.getContext('2d');
        const spinBtn = document.getElementById('spinBtn');
        const resultDiv = document.getElementById('result');
        let isSpinning = false;
        let currentAngle = 0;
        let wins = 0, losses = 0;

        // 8 Sektoren (4x Gewinn, 4x Verlust) = 50/50 Optik
        const segments = [
            { label: 'GEWINN', color: '#00ff88', type: 'win' },
            { label: 'VERLUST', color: '#ff4444', type: 'loss' },
            { label: 'GEWINN', color: '#00cc77', type: 'win' },
            { label: 'VERLUST', color: '#cc3333', type: 'loss' },
            { label: 'GEWINN', color: '#00ff88', type: 'win' },
            { label: 'VERLUST', color: '#ff4444', type: 'loss' },
            { label: 'GEWINN', color: '#00cc77', type: 'win' },
            { label: 'VERLUST', color: '#cc3333', type: 'loss' }
        ];

        const segmentAngle = (2 * Math.PI) / segments.length;

        function drawWheel(rotation) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            const radius = 190;

            segments.forEach((seg, i) => {
                const startAngle = i * segmentAngle + rotation;
                const endAngle = startAngle + segmentAngle;
                
                ctx.beginPath();
                ctx.moveTo(centerX, centerY);
                ctx.arc(centerX, centerY, radius, startAngle, endAngle);
                ctx.closePath();
                ctx.fillStyle = seg.color;
                ctx.fill();
                ctx.strokeStyle = '#fff';
                ctx.lineWidth = 2;
                ctx.stroke();

                // Text
                ctx.save();
                ctx.translate(centerX, centerY);
                ctx.rotate(startAngle + segmentAngle / 2);
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillStyle = '#fff';
                ctx.font = 'bold 18px Arial';
                ctx.shadowColor = 'rgba(0,0,0,0.5)';
                ctx.shadowBlur = 5;
                ctx.fillText(seg.label, radius * 0.65, 0);
                ctx.restore();
            });

            // Mittelpunkt
            ctx.beginPath();
            ctx.arc(centerX, centerY, 25, 0, 2 * Math.PI);
            ctx.fillStyle = '#ffd700';
            ctx.fill();
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 3;
            ctx.stroke();
        }

        function spinWheel() {
            if (isSpinning) return;
            isSpinning = true;
            spinBtn.disabled = true;
            resultDiv.textContent = '🌀 Das Rad dreht sich...';

            // Hintergrund-Anfrage für manipuliertes Ergebnis
            fetch('/spin')
                .then(response => response.json())
                .then(data => {
                    // Bestimme Ziel-Sektor basierend auf dem Ergebnis
                    const targetIndex = data.result === 'win' ? 0 : 1;
                    // Drehe so, dass ein GEWINN oder VERLUST Sektor beim Pointer landet
                    const spins = 5 + Math.random() * 5; // 5-10 Umdrehungen
                    const targetAngle = targetIndex * segmentAngle + segmentAngle / 2;
                    const finalAngle = spins * 2 * Math.PI + targetAngle;
                    
                    animateSpin(finalAngle, data);
                })
                .catch(err => {
                    console.error(err);
                    isSpinning = false;
                    spinBtn.disabled = false;
                });
        }

        function animateSpin(targetAngle, data) {
            const startAngle = currentAngle;
            const duration = 3000 + Math.random() * 1000;
            const startTime = performance.now();

            function animate(time) {
                const elapsed = time - startTime;
                const progress = Math.min(elapsed / duration, 1);
                // Easing: ease-out
                const eased = 1 - Math.pow(1 - progress, 3);
                const current = startAngle + (targetAngle - startAngle) * eased;
                
                drawWheel(current);
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    currentAngle = targetAngle;
                    isSpinning = false;
                    spinBtn.disabled = false;
                    
                    // Ergebnis anzeigen
                    if (data.result === 'win') {
                        resultDiv.innerHTML = '🎉 <span class="gewinn">GEWONNEN!</span> (50% Chance)';
                        wins++;
                    } else {
                        resultDiv.innerHTML = '😢 <span class="verlust">VERLOREN!</span> (50% Chance)';
                        losses++;
                    }
                    document.getElementById('wins').textContent = wins;
                    document.getElementById('losses').textContent = losses;
                    const total = wins + losses;
                    document.getElementById('quote').textContent = total > 0 ? (wins/total*100).toFixed(1) : '0.0';
                }
            }
            requestAnimationFrame(animate);
        }

        spinBtn.addEventListener('click', spinWheel);

        // Initial zeichnen
        drawWheel(0);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/spin')
def spin():
    # 🎯 DER TRICK: 80% Gewinn, 20% Verlust
    if random.random() < 0.8:
        return jsonify({'result': 'win'})
    else:
        return jsonify({'result': 'loss'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
