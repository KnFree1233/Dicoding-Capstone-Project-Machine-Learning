from collections import Counter
from tools import get_food_nutrition_per_gram

FOODS_NUTRITION_PER_GRAM = get_food_nutrition_per_gram()

def nutrition_estimation(food_results, real_food_sizes):
    food_estimations = []
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0
    food_class_names = food_results["food_class_names"]
    food_class_ids = food_results["food_class_ids"]

    for idx, food_size in enumerate(real_food_sizes):
        food_nutrition = {
            "calories": float(FOODS_NUTRITION_PER_GRAM[food_class_names[idx]]["calories"] * food_size["weight"]),
            "protein": float(FOODS_NUTRITION_PER_GRAM[food_class_names[idx]]["protein"] * food_size["weight"]),
            "carbs": float(FOODS_NUTRITION_PER_GRAM[food_class_names[idx]]["carbs"] * food_size["weight"]),
            "fat": float(FOODS_NUTRITION_PER_GRAM[food_class_names[idx]]["fat"] * food_size["weight"])
        }
        total_calories += food_nutrition["calories"]
        total_protein += food_nutrition["protein"]
        total_carbs += food_nutrition["carbs"]
        total_fat += food_nutrition["fat"]
        food_estimations.append({
            "class_id": int(food_class_ids[idx]),
            "class_name": food_class_names[idx],
            "nutrition": food_nutrition,
        })

    food_nutrition_results = {
        "food_count": dict(Counter(food_class_names)),
        "total_nutrition": {
            "calories": total_calories,
            "protein": total_protein,
            "carbs": total_carbs,
            "fat": total_fat
        },
        "food_estimations": food_estimations
    }
    return food_nutrition_results