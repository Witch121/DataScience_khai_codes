import csv
import re

def parse_data(filename):
    """Reads data from file and returns list of dictionaries"""
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # skip the headlines
        for row in reader:
            if len(row) == 3:
                data.append({
                    "ПІБ": row[0].strip(),
                    "ріст": row[1].strip(),
                    "вага": row[2].strip()
                })
    return data

def clean_data(data):
    """Cleans data: checks numbers, brings names into a uniform format"""
    cleaned_data = []
    for person in data:
        try:
            height = int(re.sub(r'[^0-9]', '', person['ріст']))
            weight = int(re.sub(r'[^0-9]', '', person['вага']))
            name = person['ПІБ'].title()
            cleaned_data.append({"name": name, "height": height, "weight": weight})
        except ValueError:
            continue  # Skip incorrect lines
    return cleaned_data

def calculate_bmi(data):
    """Calculates BMI and determines weight category"""
    for person in data:
        height_m = person['height'] / 100  # Convert cm to meters
        bmi = round(person['weight'] / (height_m ** 2), 2)
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
        elif 25 <= bmi < 35:
            category = "Overweight"
        else:
            category = "Obese"
        person["BMI"] = bmi
        person["Weight Category"] = category
    return data


def analyze_data(data):
    """Calculates statistical characteristics"""
    heights = [person['height'] for person in data]
    weights = [person['weight'] for person in data]
    
    avg_height = sum(heights) / len(heights)
    avg_weight = sum(weights) / len(weights)
    
    min_height, max_height = min(heights), max(heights)
    min_weight, max_weight = min(weights), max(weights)
    
    categories = [person['Weight Category'] for person in data]
    total = len(categories)
    underweight = categories.count("Underweight") / total * 100
    normal_weight = categories.count("Normal weight") / total * 100
    overweight = categories.count("Overweight") / total * 100
    obese = categories.count("Obese") / total * 100
    
    return {
        "Average Height": avg_height,
        "Average Weight": avg_weight,
        "Min Height": min_height,
        "Max Height": max_height,
        "Min Weight": min_weight,
        "Max Weight": max_weight,
        "Underweight (%)": underweight,
        "Normal Weight (%)": normal_weight,
        "Overweight (%)": overweight,
        "Obese (%)": obese
    }

def save_cleaned_data(filename, data):
    """Saves the cleaned data to a new file"""
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(["Name", "Height", "Weight", "BMI", "Weight Category"])
        for person in data:
            writer.writerow([person['name'], person['height'], person['weight'], person['BMI'], person['Weight Category']])

# Виконання коду
input_file = "LW2.txt"
output_file = "cleaned_LW2.txt"

data = parse_data(input_file)
cleaned_data = clean_data(data)
processed_data = calculate_bmi(cleaned_data)
stats = analyze_data(processed_data)

save_cleaned_data(output_file, processed_data)

print("Data analysis statistics:")
for key, value in stats.items():
    print(f"{key}: {value}")
