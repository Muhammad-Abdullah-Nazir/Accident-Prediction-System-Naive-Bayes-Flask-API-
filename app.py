from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Prior probabilities (calculated from dataset)
P_accident_yes = 4 / 10  # 0.4
P_accident_no = 6 / 10   # 0.6

# Weather probabilities
weather_probs = {
    'Rain': {
        'yes': 1/4,      # 0.25
        'no': 2/6        # 0.333
    },
    'Snow': {
        'yes': 1/4,      # 0.25
        'no': 2/6        # 0.333
    },
    'Clear': {
        'yes': 2/4,      # 0.5
        'no': 2/6        # 0.333
    }
}

# Road condition probabilities
road_probs = {
    'Good': {
        'yes': 1/4,      # 0.25
        'no': 3/6        # 0.5
    },
    'Bad': {
        'yes': 2/4,      # 0.5
        'no': 1/6        # 0.167
    },
    'Average': {
        'yes': 0.01,     # Smoothing (0 in dataset)
        'no': 2/6        # 0.333
    }
}

# Traffic condition probabilities
traffic_probs = {
    'High': {
        'yes': 3/4,      # 0.75
        'no': 1/6        # 0.167
    },
    'Normal': {
        'yes': 0.01,     # Smoothing (0 in dataset)
        'no': 3/6        # 0.5
    },
    'Light': {
        'yes': 1/4,      # 0.25
        'no': 2/6        # 0.333
    }
}

# Engine problem probabilities
engine_probs = {
    'No': {
        'yes': 2/4,      # 0.5
        'no': 4/6        # 0.667
    },
    'Yes': {
        'yes': 2/4,      # 0.5
        'no': 2/6        # 0.333
    }
}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        weather = data.get('weather')
        road = data.get('road')
        traffic = data.get('traffic')
        engine = data.get('engine')
        
        # Get probabilities for each feature
        p_weather_yes = weather_probs.get(weather, {}).get('yes', 0.01)
        p_weather_no = weather_probs.get(weather, {}).get('no', 0.01)
        
        p_road_yes = road_probs.get(road, {}).get('yes', 0.01)
        p_road_no = road_probs.get(road, {}).get('no', 0.01)
        
        p_traffic_yes = traffic_probs.get(traffic, {}).get('yes', 0.01)
        p_traffic_no = traffic_probs.get(traffic, {}).get('no', 0.01)
        
        p_engine_yes = engine_probs.get(engine, {}).get('yes', 0.01)
        p_engine_no = engine_probs.get(engine, {}).get('no', 0.01)
        
        # Calculate P(Accident=Yes | conditions)
        prob_yes = (p_weather_yes * p_road_yes * p_traffic_yes * 
                   p_engine_yes * P_accident_yes)
        
        # Calculate P(Accident=No | conditions)
        prob_no = (p_weather_no * p_road_no * p_traffic_no * 
                  p_engine_no * P_accident_no)
        
        # Normalize to get percentages
        total = prob_yes + prob_no
        if total > 0:
            prob_yes_percent = (prob_yes / total) * 100
            prob_no_percent = (prob_no / total) * 100
        else:
            prob_yes_percent = 0
            prob_no_percent = 0
        
        # Make prediction
        is_accident = prob_yes > prob_no
        prediction = "YES - Accident Likely ⚠️" if is_accident else "NO - Safe to Drive ✅"
        confidence = max(prob_yes_percent, prob_no_percent)
        
        # Prepare detailed breakdown
        breakdown = {
            'weather': {
                'value': weather,
                'p_yes': round(p_weather_yes, 4),
                'p_no': round(p_weather_no, 4)
            },
            'road': {
                'value': road,
                'p_yes': round(p_road_yes, 4),
                'p_no': round(p_road_no, 4)
            },
            'traffic': {
                'value': traffic,
                'p_yes': round(p_traffic_yes, 4),
                'p_no': round(p_traffic_no, 4)
            },
            'engine': {
                'value': engine,
                'p_yes': round(p_engine_yes, 4),
                'p_no': round(p_engine_no, 4)
            }
        }
        
        return jsonify({
            'prediction': prediction,
            'is_accident': is_accident,
            'prob_yes_raw': round(prob_yes, 8),
            'prob_no_raw': round(prob_no, 8),
            'prob_yes_percent': round(prob_yes_percent, 2),
            'prob_no_percent': round(prob_no_percent, 2),
            'confidence': round(confidence, 2),
            'breakdown': breakdown
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/', methods=['GET'])
def home():
    return """
    <h1>🚗 Accident Prediction API</h1>
    <p>Backend is running successfully!</p>
    <p>Dataset: 10 records (4 accidents, 6 safe)</p>
    """

if __name__ == '__main__':
    print("=" * 60)
    print("🚗 ACCIDENT PREDICTION SERVER STARTING")
    print("=" * 60)
    print("\nDataset Statistics:")
    print(f"  Total Records: 10")
    print(f"  Accidents (Yes): 4 (40%)")
    print(f"  Safe Drives (No): 6 (60%)")
    print(f"\nServer running on: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, port=5000)