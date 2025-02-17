import streamlit as st
import numpy as np
import pickle
import requests
import os

# Load the trained model
loaded_model = pickle.load(open('crop_recomendation_model.pkl', 'rb'))


# Check if the model file exists

# Fertilizer recommendations for each crop
fertilizer_dict = {
    'rice': [
        {"name": "Urea", "description": "Boosts vegetative growth, apply in 2-3 split doses."},
        {"name": "DAP (Di-Ammonium Phosphate)", "description": "Strengthens roots, apply before sowing."},
        {"name": "MOP (Muriate of Potash)", "description": "Enhances disease resistance, apply in early growth stage."},
        {"name": "SSP (Single Super Phosphate)", "description": "Provides phosphorus for early root growth."}
    ],

    'maize': [
        {"name": "Urea", "description": "Promotes leaf and stem growth, apply in two doses."},
        {"name": "DAP", "description": "Supports grain yield, apply at planting."},
        {"name": "NPK (20:20:0)", "description": "Balanced nutrition, use as basal fertilizer."}
    ],

    'chickpea': [
        {"name": "DAP", "description": "Encourages root growth, apply at sowing."},
        {"name": "SSP", "description": "Enhances nodulation, use as basal dose."},
        {"name": "Bio-fertilizers (Rhizobium)", "description": "Improves nitrogen fixation."}
    ],

    'kidneybeans': [
        {"name": "DAP", "description": "Boosts root development, apply at sowing."},
        {"name": "Rhizobium Inoculants", "description": "Enhances nitrogen fixation."}
    ],

    'pigeonpeas': [
        {"name": "SSP", "description": "Supports phosphorus needs, apply at sowing."},
        {"name": "Rock Phosphate", "description": "Slow-release phosphorus for sustained growth."},
        {"name": "Bio-fertilizers", "description": "Increases nutrient absorption."}
    ],

    'mothbeans': [
        {"name": "DAP", "description": "Promotes early growth, apply at sowing."},
        {"name": "NPK (20:20:0)", "description": "Balanced nutrients for growth."},
        {"name": "Bio-fertilizers", "description": "Enhances nitrogen-fixing ability."}
    ],

    'mungbean': [
        {"name": "DAP", "description": "Encourages early root growth."},
        {"name": "SSP", "description": "Supplies phosphorus, use as basal fertilizer."},
        {"name": "Rhizobium Culture", "description": "Helps in nitrogen fixation."}
    ],

    'blackgram': [
        {"name": "DAP", "description": "Provides phosphorus for root growth."},
        {"name": "SSP", "description": "Improves flowering and yield."},
        {"name": "Phosphorus Solubilizing Bacteria (PSB)", "description": "Enhances phosphorus availability."}
    ],

    'lentil': [
        {"name": "DAP", "description": "Strengthens root system, apply at sowing."},
        {"name": "SSP", "description": "Supports phosphorus needs."},
        {"name": "Rhizobium Bio-fertilizers", "description": "Aids nitrogen fixation."}
    ],

    'pomegranate': [
        {"name": "Urea", "description": "Boosts vegetative growth."},
        {"name": "MOP", "description": "Enhances fruit quality and disease resistance."},
        {"name": "SSP", "description": "Supplies phosphorus for flowering."}
    ],

    'banana': [
        {"name": "Urea", "description": "Increases foliage development."},
        {"name": "DAP", "description": "Supports root growth, apply at planting."},
        {"name": "MOP", "description": "Improves fruit development and disease resistance."}
    ],

    'mango': [
        {"name": "Farmyard Manure", "description": "Organic matter improves soil fertility."},
        {"name": "SSP", "description": "Strengthens root development."},
        {"name": "Potash Fertilizers", "description": "Enhances fruit quality."}
    ],

    'grapes': [
        {"name": "DAP", "description": "Encourages flowering and fruiting."},
        {"name": "MOP", "description": "Improves fruit quality and disease resistance."},
        {"name": "NPK (19:19:19)", "description": "Balanced nutrients for growth."}
    ],

    'watermelon': [
        {"name": "Urea", "description": "Supports vine growth."},
        {"name": "MOP", "description": "Enhances fruit development."},
        {"name": "Boron Fertilizers", "description": "Prevents fruit cracking."}
    ],

    'muskmelon': [
        {"name": "NPK (20:20:20)", "description": "Ensures balanced nutrient supply."},
        {"name": "Boron Fertilizers", "description": "Improves fruit setting."}
    ],

    'apple': [
        {"name": "Farmyard Manure", "description": "Improves soil structure."},
        {"name": "NPK (10:10:10)", "description": "Provides balanced nutrition for tree growth."}
    ],

    'orange': [
        {"name": "NPK (15:15:15)", "description": "Balanced nutrients for fruit formation."},
        {"name": "Zinc Sulphate", "description": "Prevents fruit drop and improves quality."}
    ],

    'papaya': [
        {"name": "Urea", "description": "Supports rapid growth."},
        {"name": "SSP", "description": "Provides phosphorus for flowering."},
        {"name": "Potash Fertilizers", "description": "Enhances fruit quality."}
    ],

    'coconut': [
        {"name": "Urea", "description": "Increases leaf production."},
        {"name": "MOP", "description": "Improves nut size and quality."},
        {"name": "Boron Fertilizers", "description": "Prevents nut splitting."}
    ],

    'cotton': [
        {"name": "Urea", "description": "Enhances vegetative growth."},
        {"name": "SSP", "description": "Supports early root establishment."},
        {"name": "NPK (20:20:0)", "description": "Balanced nutrition for fiber development."}
    ],

    'jute': [
        {"name": "Urea", "description": "Promotes vegetative growth."},
        {"name": "SSP", "description": "Provides phosphorus for root growth."},
        {"name": "Potash Fertilizers", "description": "Strengthens fiber quality."}
    ],

    'coffee': [
        {"name": "Urea", "description": "Increases leaf development."},
        {"name": "SSP", "description": "Supports flowering."},
        {"name": "Potash", "description": "Enhances bean quality."},
        {"name": "Micronutrients", "description": "Essential for flavor and aroma development."}
    ]
}


crop_guidance = {
    "rice": [
        "🌱 **Soil:** Clayey, loamy soil with good water retention.",
        "🌡 **Climate:** Warm and humid; temperature between 20-35°C.",
        "💦 **Watering:** Requires standing water; maintain a flooded field.",
        "⚠️ **Special Care:** Proper weed control and pest management needed."
    ],
    "maize": [
        "🌱 **Soil:** Well-drained loamy soil with pH 5.5-7.",
        "🌡 **Climate:** Requires warm temperatures (18-27°C).",
        "💦 **Watering:** Moderate water requirement; avoid waterlogging.",
        "⚠️ **Special Care:** Apply fertilizers in stages for better yields."
    ],
    "chickpea": [
        "🌱 **Soil:** Sandy loam with good drainage.",
        "🌡 **Climate:** Prefers cool, dry weather (20-25°C).",
        "💦 **Watering:** Needs less water; avoid excessive moisture.",
        "⚠️ **Special Care:** Use Rhizobium inoculation for better nitrogen fixation."
    ],
    "kidneybeans": [
        "🌱 **Soil:** Well-drained loamy soil with organic matter.",
        "🌡 **Climate:** Prefers moderate temperatures (15-25°C).",
        "💦 **Watering:** Needs consistent moisture but not waterlogging.",
        "⚠️ **Special Care:** Rotate crops to prevent soil depletion."
    ],
    "pigeonpeas": [
        "🌱 **Soil:** Well-drained sandy loam soil.",
        "🌡 **Climate:** Grows well in warm conditions (25-35°C).",
        "💦 **Watering:** Drought-resistant but needs occasional watering.",
        "⚠️ **Special Care:** Protect from heavy rains during flowering."
    ],
    "mothbeans": [
        "🌱 **Soil:** Sandy or loamy soil with good drainage.",
        "🌡 **Climate:** Thrives in hot and dry conditions (25-40°C).",
        "💦 **Watering:** Minimal water needed; drought-resistant.",
        "⚠️ **Special Care:** Avoid overwatering as roots are shallow."
    ],
    "mungbean": [
        "🌱 **Soil:** Sandy loam with a pH of 6.2-7.2.",
        "🌡 **Climate:** Prefers warm temperatures (20-30°C).",
        "💦 **Watering:** Requires moderate moisture; avoid excess.",
        "⚠️ **Special Care:** Use Rhizobium bio-fertilizers for better yields."
    ],
    "blackgram": [
        "🌱 **Soil:** Well-drained sandy loam soil.",
        "🌡 **Climate:** Requires warm and humid weather (25-30°C).",
        "💦 **Watering:** Needs less water; drought-resistant.",
        "⚠️ **Special Care:** Protect from excess moisture during pod formation."
    ],
    "lentil": [
        "🌱 **Soil:** Clay loam or sandy loam with good drainage.",
        "🌡 **Climate:** Prefers cool temperatures (18-25°C).",
        "💦 **Watering:** Minimal irrigation required; avoid excess moisture.",
        "⚠️ **Special Care:** Use bio-fertilizers for better nitrogen fixation."
    ],
    "pomegranate": [
        "🌱 **Soil:** Well-drained sandy loam soil.",
        "🌡 **Climate:** Thrives in hot, arid climates (25-35°C).",
        "💦 **Watering:** Requires deep watering every 7-10 days.",
        "⚠️ **Special Care:** Prune regularly to improve air circulation."
    ],
    "banana": [
        "🌱 **Soil:** Well-drained loamy soil with good organic content.",
        "🌡 **Climate:** Warm and humid (25-35°C).",
        "💦 **Watering:** Frequent irrigation required, avoid waterlogging.",
        "⚠️ **Special Care:** Protect from strong winds; use potassium-based fertilizers."
    ],
    "mango": [
        "🌱 **Soil:** Well-drained sandy loam with good fertility.",
        "🌡 **Climate:** Prefers warm temperatures (25-35°C).",
        "💦 **Watering:** Moderate irrigation; reduce during flowering.",
        "⚠️ **Special Care:** Prune trees to maintain good air circulation."
    ],
    "grapes": [
        "🌱 **Soil:** Well-drained loamy soil, pH 6-7.5.",
        "🌡 **Climate:** Requires warm, dry conditions (20-35°C).",
        "💦 **Watering:** Drip irrigation is preferred.",
        "⚠️ **Special Care:** Support vines with trellises for better growth."
    ],
    "watermelon": [
        "🌱 **Soil:** Sandy loam soil, well-drained.",
        "🌡 **Climate:** Prefers hot, dry climates (25-40°C).",
        "💦 **Watering:** Regular irrigation needed but avoid overwatering.",
        "⚠️ **Special Care:** Use mulching to retain moisture."
    ],
    "muskmelon": [
        "🌱 **Soil:** Sandy loam, rich in organic matter.",
        "🌡 **Climate:** Requires warm weather (25-35°C).",
        "💦 **Watering:** Regular but controlled irrigation.",
        "⚠️ **Special Care:** Avoid excess moisture to prevent fungal diseases."
    ],
    "apple": [
        "🌱 **Soil:** Loamy soil with good drainage, pH 5.5-6.5.",
        "🌡 **Climate:** Requires cold winters and mild summers (5-25°C).",
        "💦 **Watering:** Moderate irrigation; avoid excess moisture.",
        "⚠️ **Special Care:** Prune trees regularly for better fruit production."
    ],
    "orange": [
        "🌱 **Soil:** Well-drained sandy loam, pH 5.5-7.5.",
        "🌡 **Climate:** Prefers warm temperatures (15-30°C).",
        "💦 **Watering:** Regular watering; avoid drought stress.",
        "⚠️ **Special Care:** Protect from frost and extreme heat."
    ],
    "papaya": [
        "🌱 **Soil:** Well-drained sandy loam with good fertility.",
        "🌡 **Climate:** Requires warm weather (22-32°C).",
        "💦 **Watering:** Frequent but controlled irrigation.",
        "⚠️ **Special Care:** Avoid waterlogging; provide wind protection."
    ],
    "coconut": [
        "🌱 **Soil:** Sandy loam or coastal soil with good drainage.",
        "🌡 **Climate:** Requires warm, humid conditions (25-35°C).",
        "💦 **Watering:** Requires consistent moisture.",
        "⚠️ **Special Care:** Mulch around the base to retain soil moisture."
    ],
    "cotton": [
        "🌱 **Soil:** Well-drained black soil, pH 6-7.5.",
        "🌡 **Climate:** Requires warm temperatures (25-35°C).",
        "💦 **Watering:** Requires irrigation during flowering.",
        "⚠️ **Special Care:** Use proper pest control measures."
    ],
    "jute": [
        "🌱 **Soil:** Sandy loam or clayey soil with good moisture retention.",
        "🌡 **Climate:** Prefers hot and humid conditions (25-35°C).",
        "💦 **Watering:** Requires good soil moisture; avoid waterlogging.",
        "⚠️ **Special Care:** Maintain high humidity for better fiber quality."
    ],
    "coffee": [
        "🌱 **Soil:** Well-drained volcanic soil, pH 6-6.5.",
        "🌡 **Climate:** Prefers cool, humid climates (15-25°C).",
        "💦 **Watering:** Requires frequent watering but avoid waterlogging.",
        "⚠️ **Special Care:** Provide shade for young plants."
    ]
}




# Function to fetch current weather data
def get_current_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        humidity = main["humidity"]
        return temperature, humidity
    else:
        st.error("City Not Found")
        return None, None

# Crop prediction function
def crop_prediction(input_data):
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    predicted_crop = loaded_model.predict(input_data_reshaped)[0]
    return predicted_crop

# Streamlit app
def main():
    st.title("🌱 Crop & Fertilizer Recommendation System")
    st.write("Enter the soil and weather details:")

    # Input fields for features
    n = st.slider("🌾 Nitrogen", min_value=0, max_value=140, value=30)
    p = st.slider("🌱 Phosphorous", min_value=5, max_value=145, value=30)
    k = st.slider("🌿 Potassium", min_value=5, max_value=205, value=30)
    ph = st.number_input("⚖️ Soil pH", min_value=3.50, max_value=9.93, value=5.00, format="%.2f")
    rain = st.number_input("🌧 Rainfall (mm)", min_value=20.21, max_value=298.56, value=25.00, format="%.2f")

    # Fetch current temperature and humidity
    api_key = "a348c64893ec6f58d83dd2e60cbadc58"  # Replace with your OpenWeatherMap API key
    city = "Coimbatore"
    temp, hum = get_current_weather(city, api_key)

    if temp is not None and hum is not None:
        st.write(f"🌡 **Current Temperature:** {temp}°C")
        st.write(f"💧 **Current Humidity:** {hum}%")

        if st.button('🔍 Recommend Crop & Fertilizer'):
            # Predict crop
            recommended_crop = crop_prediction([n, p, k, temp, hum, ph, rain])
            # Get fertilizer recommendation
            recommended_fertilizer = fertilizer_dict.get(recommended_crop, "No recommendation available")

            # Display recommendations
            st.success(f"🌾 **Recommended Crop:** {recommended_crop.upper()}")
            st.subheader(f"🧪 Recommended Fertilizers for {recommended_crop.capitalize()}:")

            for fertilizer in recommended_fertilizer:
                st.markdown(f"**🔹 {fertilizer['name']}**: {fertilizer['description']}")

            st.subheader("🌾 **Crop Guidance:**")

            for point in crop_guidance[recommended_crop]:
                st.write(point)

    else:
        st.error("Unable to fetch current weather data. Please enter manually.")

if __name__ == "__main__":
    main()
