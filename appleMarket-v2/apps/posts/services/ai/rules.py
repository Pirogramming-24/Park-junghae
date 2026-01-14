import re

def to_number(text):
    nums = re.findall(r"\d+\.?\d*", text)
    if not nums:
        return None
    return float(nums[0])

def parse_nutrition(ocr_items):
    texts = [item["text"] for item in ocr_items]

    result = {
        "kcal": None,
        "carbs": None,
        "protein": None,
        "fat": None
    }

    kcal_found = False

    for i, t in enumerate(texts):
        t = t.replace(" ", "").lower()

        if "kcal" in t and not kcal_found:
            if i > 0:
                v = to_number(texts[i-1])
                if v:
                    result["kcal"] = v
                    kcal_found = True
                    continue

            if i+1 < len(texts):
                v = to_number(texts[i+1])
                if v:
                    result["kcal"] = v
                    kcal_found = True

        if "탄수화물" in t and i+1 < len(texts):
            result["carbs"] = to_number(texts[i+1])

        if "단백질" in t and i+1 < len(texts):
            result["protein"] = to_number(texts[i+1])

        if t == "지방" and i+1 < len(texts):
            result["fat"] = to_number(texts[i+1])

    return result
