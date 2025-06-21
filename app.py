from flask import Flask, render_template, request, jsonify, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/task')
def task():
    total_points = session.get('points', 0)
    return render_template('task.html', points=total_points)
  


@app.route('/cart')
def cart():
    total_points = session.get('points', 0)
    return render_template('cart.html', points=total_points)

@app.route('/reset_points', methods=['POST'])
def reset_points():
    session['points'] = 0
    return jsonify({'success': True, 'total_points': 0})





@app.route('/earn_points', methods=['POST'])
def earn_points():
    data = request.get_json()
    earned = int(data.get('points', 0))
    current_points = session.get('points', 0)
    current_points += earned
    session['points'] = current_points
    return jsonify({'total_points': current_points})

@app.route('/redeem', methods=['POST'])
def redeem():
    data = request.get_json()
    cost = int(data.get('cost', 0))
    current_points = session.get('points', 0)

    if current_points >= cost:
        current_points -= cost
        session['points'] = current_points
        return jsonify({'success': True, 'total_points': current_points})
    else:
        return jsonify({'success': False, 'message': 'Not enough points', 'total_points': current_points})

if __name__ == '__main__':
    app.run(debug=True)
