from raw_to_dataset import load_gesture_xyz


# Included sample data paths (3D building wireframes)
concert_test_inp = "util/sample_data/concert_sample/concert_sample_default.json"
apt_verticalL = "util/sample_data/apt_verticalL_sample/apt_verticalL_sample_default2.json"
apt1 = "util/sample_data/apt1_sample/apt1_sample_1.json"
concert = "util/sample_data/concert_sample/concert_sample_default2.json"
house1 = "util/sample_data/house1_sample/house1_sample_default2.json"


if __name__ == "__main__":
    JSON_FILEPATH = house1

    points = load_gesture_xyz(JSON_FILEPATH)

    result = "new List<Vector3>\n{\n"
    for i, point in enumerate(points):
        x, y, z = point
        # Format floats with 'f' suffix for C#
        
        result += f"    new Vector3({x}f, {y}f, {z}f)"
        
        # Add comma if not the last element
        if i < len(points) - 1:
            result += ","
        
        result += "\n"
        
    result += "};"

    print(result)
