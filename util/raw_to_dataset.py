import os
import json
import numpy as np

def resample_points(points, num_points):
    """
    Resamples a list of points to exactly num_points
        - linear interpolation over cumulative path distance.
        - For 1D gestures/strokes
    """
    pts = np.array(points)
    N = len(pts)

    if N == 0:
        return np.zeros((num_points, 3))  # edge case
    if N == 1:
        return np.repeat(pts, num_points, axis=0) # repeat

    # Compute cumulative distance along the path
    deltas = pts[1:] - pts[:-1]
    segment_lengths = np.linalg.norm(deltas, axis=1)
    cumulative = np.insert(np.cumsum(segment_lengths), 0, 0)
    total_len = cumulative[-1]

    # Create equally spaced target distances
    target_distances = np.linspace(0, total_len, num_points)

    # Interpolate separately for x, y, z
    resampled = np.zeros((num_points, 3))
    for dim in range(3):
        resampled[:, dim] = np.interp(
            target_distances,
            cumulative,
            pts[:, dim]
        )

    return resampled.tolist()


def sample_points_fixed(points, N=128, seed=None):
    """
    Uniformly sample a point list to exactly N points.
    - If len(points) > N: uniform downsample
    - If len(points) < N: randomly repeat some points
    """
    if seed is not None:
        np.random.seed(seed)

    points = np.array(points)
    L = len(points)

    if L == 0:
        raise ValueError("Cannot sample from an empty point list.")

    # Case 1: More than N, downsample
    if L > N:
        idx = np.linspace(0, L - 1, N, dtype=int)
        return points[idx].tolist()

    # Case 2: Less than N, pad with random repeats
    if L < N:
        needed = N - L
        repeat_idx = np.random.choice(L, size=needed, replace=True)

        padded = np.concatenate([points, points[repeat_idx]], axis=0)
        return padded.tolist()
    
    # Case 3: Already exactly N
    return points.tolist()


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
    

def load_gesture_xyz(filepath):
    """Load a single gesture JSON file and return list of (x, y, z) points."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    points = [(p['x'], p['y'], p['z']) for p in data['points']]

    # Preprocessing + normalization steps
    points = set_first_as_origin(points) # Take 1st point as (0,0,0), update other points relative
    points = sample_points_fixed(points, 128) # Resize to 128 points
                
    return points


def build_npz_dataset(dataset_root, output_file='gesture_dataset.npz'):
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
                points = load_gesture_xyz(filepath)

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
