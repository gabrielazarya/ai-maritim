import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Load data from Excel
shipping_data = pd.read_excel("shipping_data.xlsx")  # Adjust filename accordingly

# Generate universe variables
weight = ctrl.Antecedent(np.arange(0, 10, 0.1), 'weight')
length = ctrl.Antecedent(np.arange(0, 2, 0.01), 'length')
width = ctrl.Antecedent(np.arange(0, 2, 0.01), 'width')
height = ctrl.Antecedent(np.arange(0, 2, 0.01), 'height')
price = ctrl.Consequent(np.arange(0, 200, 1), 'price')

# Membership functions
weight['low'] = fuzz.trimf(weight.universe, [0, 2, 5])
weight['medium'] = fuzz.trimf(weight.universe, [2, 5, 8])
weight['high'] = fuzz.trimf(weight.universe, [5, 8, 10])

length.automf(3)
width.automf(3)
height.automf(3)

price['low'] = fuzz.trimf(price.universe, [0, 50, 100])
price['medium'] = fuzz.trimf(price.universe, [50, 100, 150])
price['high'] = fuzz.trimf(price.universe, [100, 150, 200])

# Define rules
rule1 = ctrl.Rule(weight['low'] & length['poor'] & width['poor'] & height['poor'], price['low'])
rule2 = ctrl.Rule(weight['medium'] & length['average'] & width['average'] & height['average'], price['medium'])
rule3 = ctrl.Rule(weight['high'] & length['good'] & width['good'] & height['good'], price['high'])

# Control System
price_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
pricing = ctrl.ControlSystemSimulation(price_ctrl)

# Fuzzification function
def fuzzy_price(weight_val, length_val, width_val, height_val):
    pricing.input['weight'] = weight_val
    pricing.input['length'] = length_val
    pricing.input['width'] = width_val
    pricing.input['height'] = height_val
    pricing.compute()
    return pricing.output['price']

# Manual input
weight_input = float(input("Enter weight (kg): "))
length_input = float(input("Enter length (m): "))
width_input = float(input("Enter width (m): "))
height_input = float(input("Enter height (m): "))

# Find actual price from Excel
actual_price = shipping_data[(shipping_data['weight (kg)'] == weight_input) &
                             (shipping_data['length (m)'] == length_input) &
                             (shipping_data['width (m)'] == width_input) &
                             (shipping_data['height (m)'] == height_input)]['price ($)'].values[0]

# Fuzzy price calculation
fuzzy_result = fuzzy_price(weight_input, length_input, width_input, height_input)

# Accuracy calculation
accuracy = abs(actual_price - fuzzy_result) / actual_price * 100

# Print results
print("Actual Price from Excel: $", actual_price)
print("Fuzzy Price: $", fuzzy_result)
print("Accuracy: %.2f%%" % accuracy)
