## (WIP) XR_GestureRecognition 
(Note: This is not a fully released version of the project, but is currently kept public for various reasons. It should release soon once some final training data is captured!)  
This is an XR gesture recognition tool for Unity, useful for drawn 3D shape/drawing recognition or gesture recognition for order-invariant gestures. It uses a Siamese neural network which learns a similarity function for comparing 3D drawings as opposed to classification of a set amount of shapes. This means you can use the model straight out of the box without needing to train the model on custom 3D shapes and even create new gestures on-the-fly during runtime.

As mentioned, this is a work-in-progress. The end goal is to train a generalized tool for gesture recognition and provide an interface for training the model.

The model is also order-invariant, so it ignores the drawn order of a shape's points. For example, a square will be represented the same no matter the order its 4 edges are drawn in, and a circle drawn clockwise is equivalent to one drawn counter-clockwise. This is done by using pairwise distance matrices as input to the model instead of a sequenced 1D list of points.
