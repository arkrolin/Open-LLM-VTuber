"""
Script to update tapMotions in model_dict.json with all HitAreas from yksl2d.model3.json
"""

import json
from pathlib import Path


def main():
    # File paths
    model3_path = Path("live2d-models/yksqipao/yksl2d.model3.json")
    model_dict_path = Path("model_dict.json")

    # Read the model3 file
    print(f"📖 Reading {model3_path}...")
    with open(model3_path, "r", encoding="utf-8") as f:
        model3_data = json.load(f)

    # Extract all HitAreas Ids
    hit_areas = model3_data.get("HitAreas", [])
    print(f"✅ Found {len(hit_areas)} HitAreas")

    # Create tapMotions dictionary
    tap_motions = {}
    for area in hit_areas:
        area_id = area.get("Id")
        if area_id:
            tap_motions[area_id] = {"Tap": 1}

    print(f"✅ Created {len(tap_motions)} tapMotion entries")

    # Read model_dict.json
    print(f"\n📖 Reading {model_dict_path}...")
    with open(model_dict_path, "r", encoding="utf-8") as f:
        model_dict = json.load(f)

    # Update the second item (yksqipao)
    if len(model_dict) >= 2:
        model_dict[1]["tapMotions"] = tap_motions
        print(f"✅ Updated tapMotions for '{model_dict[1]['name']}'")
    else:
        print("❌ Error: model_dict.json doesn't have a second item")
        return

    # Write back to model_dict.json
    print(f"\n💾 Writing updated data to {model_dict_path}...")
    with open(model_dict_path, "w", encoding="utf-8") as f:
        json.dump(model_dict, f, indent=4, ensure_ascii=False)

    print(f"✨ Done! Successfully updated {len(tap_motions)} tapMotions entries")


if __name__ == "__main__":
    main()
