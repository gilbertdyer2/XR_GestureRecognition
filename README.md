## (WIP) XR_GestureRecognition 
This is an XR gesture recognition tool for Unity, useful for drawn 3D shape/drawing recognition or gesture recognition for order-invariant gestures. It uses a Siamese neural network which learns a similarity function for comparing 3D drawings as opposed to classification of a set amount of shapes. This means you can use the model straight out of the box without needing to train the model on custom 3D shapes and even create new gestures on-the-fly during runtime.

The model is also order-invariant, so it ignores the drawn order of a shape's points. For example, a square will be represented the same no matter the order its 4 edges are drawn in, and a circle drawn clockwise is equivalent to one drawn counter-clockwise. This is done by using pairwise distance matrices as input to the model instead of a sequenced 1D list of points.

As mentioned, this is a work-in-progress. The end goal is to train a generalized tool for gesture recognition and provide an interface for training the model yourself.


## Note for CSCI4366:
Specific to CSCI4366, the scope of this project is narrowed on applying the tool to a simple city-builder AR game for the Meta Quest, PicoTown. A core mechanic of the game is to allow the player to draw a custom building wireframe, then spawn in the closest matching building asset to the shape. As of now, the dataset and models are a bit "overfit" to wireframe drawings of various building-like shapes (house, apartment, etc.. See gesture_dataset_RAW) due to data collection being pretty tedious (the dataset is also very small currently, but still seems to work well for the game).

Unfortunately the game itself is not finished as of the most recent commit and also requires a Meta Quest to run, but the model architecture is fully complete. I've provided a script (visualize_data) in utils/ to visualize the data the model was trained on, and a script to test the model's effectiveness on(test_trained_fromJSON) sample data of drawings of buildings, separately recorded from the dataset.


## Project Contributors:
Gilbert Dyer (@gilbertdyer2)
