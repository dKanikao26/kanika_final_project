import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the trained model
with open('hhmodel.pkl', 'rb') as file:
    model = pickle.load(file)

# Customized ranges for each feature
custom_ranges = {
    'Engine rpm': (61.0, 3000.0),
    'Lub oil pressure': (0.003384, 7.265566),
    'Fuel pressure': (0.003187, 21.138326),
    'Coolant pressure': (0.002483, 7.478505),
    'lub oil temp': (71.321974, 89.580796),
    'Coolant temp': (61.673325, 195.527912),
    'Temperature_difference': (-22.669427, 119.008526)
}

# Feature descriptions for sidebar
feature_descriptions = {
    'Engine rpm': 'Revolution per minute of the engine.',
    'Lub oil pressure': 'Pressure of the lubricating oil.',
    'Fuel pressure': 'Pressure of the fuel.',
    'Coolant pressure': 'Pressure of the coolant.',
    'lub oil temp': 'Temperature of the lubricating oil.',
    'Coolant temp': 'Temperature of the coolant.',
    'Temperature_difference': 'Temperature difference between components.'
}


def get_custom_parameter_messages(params):
    messages = []
    engine_rpm, lub_oil_pressure, fuel_pressure, coolant_pressure, lub_oil_temp, coolant_temp, temp_difference = params

    if engine_rpm < 1266:
        messages.append("⚠️ Engine RPM is too low. This may cause stalling or performance issues.")

    if lub_oil_pressure < 1.0:
        messages.append("🛢️ Low Lubricating Oil Pressure detected — check for possible leaks or pump issues.")

    if fuel_pressure < 1.0:
        messages.append("⛽ Fuel Pressure is unusually low. Engine may not get enough fuel.")

    if coolant_pressure < 1.0:
        messages.append("🌡️ Coolant Pressure is low. Risk of engine overheating.")
   
    if lub_oil_temp > 85:
        messages.append("🔥 Lubricating Oil Temperature is high. May indicate overheating.")

    if coolant_temp > 150:
        messages.append("🔥 Coolant Temperature is very high. Stop engine immediately to prevent damage.")

    if temp_difference > 80:
        messages.append("⚠️ High Temperature Difference detected — uneven heating could cause mechanical stress.")

    if fuel_pressure > 19.72:
        messages.append("high pressure .")

    return messages

def predict_condition(features):
    input_data = np.array(features).reshape(1, -1)
    prediction = model.predict(input_data)[0]
    # Confidence removed as per request
    return prediction

def main():
    st.title("Engine Condition Prediction")

    st.sidebar.title("Feature Descriptions")
    for feature, desc in feature_descriptions.items():
        st.sidebar.markdown(f"**{feature}:** {desc}")
    st.sidebar.markdown("---")

    # Input sliders
    engine_rpm = st.slider("Engine RPM", 
                           min_value=float(custom_ranges['Engine rpm'][0]), 
                           max_value=float(custom_ranges['Engine rpm'][1]), 
                           value=float((custom_ranges['Engine rpm'][0] + custom_ranges['Engine rpm'][1]) / 2),
                           step=1.0)
    
    lub_oil_pressure = st.slider("Lub Oil Pressure", 
                                 min_value=float(custom_ranges['Lub oil pressure'][0]), 
                                 max_value=float(custom_ranges['Lub oil pressure'][1]), 
                                 value=float((custom_ranges['Lub oil pressure'][0] + custom_ranges['Lub oil pressure'][1]) / 2),
                                 step=0.01)
    
    fuel_pressure = st.slider("Fuel Pressure", 
                              min_value=float(custom_ranges['Fuel pressure'][0]), 
                              max_value=float(custom_ranges['Fuel pressure'][1]), 
                              value=float((custom_ranges['Fuel pressure'][0] + custom_ranges['Fuel pressure'][1]) / 2),
                              step=0.01)
    
    coolant_pressure = st.slider("Coolant Pressure", 
                                 min_value=float(custom_ranges['Coolant pressure'][0]), 
                                 max_value=float(custom_ranges['Coolant pressure'][1]), 
                                 value=float((custom_ranges['Coolant pressure'][0] + custom_ranges['Coolant pressure'][1]) / 2),
                                 step=0.01)
    
    lub_oil_temp = st.slider("Lub Oil Temperature", 
                             min_value=float(custom_ranges['lub oil temp'][0]), 
                             max_value=float(custom_ranges['lub oil temp'][1]), 
                             value=float((custom_ranges['lub oil temp'][0] + custom_ranges['lub oil temp'][1]) / 2),
                             step=0.01)
    
    coolant_temp = st.slider("Coolant Temperature", 
                             min_value=float(custom_ranges['Coolant temp'][0]), 
                             max_value=float(custom_ranges['Coolant temp'][1]), 
                             value=float((custom_ranges['Coolant temp'][0] + custom_ranges['Coolant temp'][1]) / 2),
                             step=0.01)
    
    temp_difference = st.slider("Temperature Difference", 
                                min_value=float(custom_ranges['Temperature_difference'][0]), 
                                max_value=float(custom_ranges['Temperature_difference'][1]), 
                                value=float((custom_ranges['Temperature_difference'][0] + custom_ranges['Temperature_difference'][1]) / 2),
                                step=0.01)

    if st.button("Predict Engine Condition"):
        features = [
            engine_rpm,
            lub_oil_pressure,
            fuel_pressure,
            coolant_pressure,
            lub_oil_temp,
            coolant_temp,
            temp_difference
        ]

        result = predict_condition(features)

        if result == 0:
            st.info("The engine is predicted to be in a normal condition.")
        else:
            st.warning("Warning! Please investigate further")

        

      
        # Show input data visualization
        st.subheader("Input Sensor Values")
        sensor_df = pd.DataFrame({
            'Sensor': list(feature_descriptions.keys()),
            'Value': features
        })
        st.bar_chart(sensor_df.set_index('Sensor'))

if __name__ == "__main__":
    main() 