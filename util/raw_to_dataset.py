import os
import json
import numpy as np

def sort_by_centroid(points):
    """Sort a list of points by distance from their centroid."""
    points_arr = np.array(points)  # shape: (N,3)
    centroid = np.mean(points_arr, axis=0)
    distances = np.linalg.norm(points_arr - centroid, axis=1)
    sorted_indices = np.argsort(distances)
    return points_arr[sorted_indices].tolist()

def get_centroid(points):
    points_arr = np.array(points)
    return np.mean(points_arr, axis=0)


def set_first_as_origin(points):
    """Treat first point as (0,0,0) - Subtracts first point value from every point."""
    points_copy = points.copy()
    origin = (points_copy[0][0], points_copy[0][1], points_copy[0][2])

    for i in range(len(points_copy)):
        modified = (
            points_copy[i][0] - origin[0],
            points_copy[i][1] - origin[1],
            points_copy[i][2] - origin[2]
        )
        points_copy[i] = modified

    return points_copy
    

def load_gesture_xyz(filepath, use_centroid=True):
    """Load a single gesture JSON file and return list of (x, y, z) points."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    points = [(p['x'], p['y'], p['z']) for p in data['points']]

    # Preprocessing + normalization steps
    points = set_first_as_origin(points) # Take 1st point as (0,0,0), update other points relative

    if (use_centroid):
        points = sort_by_centroid(points)
                
    return points


def build_npz_dataset(dataset_root, output_file='gesture_dataset.npz', use_centroid=True):
    """
    Loads gesture dataset from folders and saves as a .npz file.
    
    Returns:
        X: list of gestures (variable length)
        y: integer labels for gestures
        class_to_label: dict mapping class name -> integer
    """
    X = []
    y = []
    class_to_label = {}
    current_label = 0
    
    for gesture_class in sorted(os.listdir(dataset_root)):
        class_path = os.path.join(dataset_root, gesture_class)
        if not os.path.isdir(class_path):
            continue # skip non-folders
            
        class_to_label[gesture_class] = current_label
        
        for file_name in os.listdir(class_path):
            if file_name.endswith('.json'):
                filepath = os.path.join(class_path, file_name)
                points = load_gesture_xyz(filepath, use_centroid=True)

                if points:
                    X.append(points)
                    y.append(current_label)
        
        current_label += 1
    print("Saving dataset...")
    # Save as .npz in root folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, '..', output_file) # save into root
    np.savez(
        output_path,
        X=np.array(X, dtype=object), # needs to be object?
        y=np.array(y),
        class_to_label=class_to_label
        )
    print(f"Saved dataset to {output_file}")
    print(f"Classes: {class_to_label}")
    print(f"Total gestures: {len(X)}")
    return X, y, class_to_label

if __name__ == "__main__":
    # dataset_root = os.path.join('..', 'gesture_dataset_RAW')
    dataset_root = 'gesture_dataset_RAW'
    X, y, class_to_label = build_npz_dataset(dataset_root, output_file='gesture_dataset.npz')
