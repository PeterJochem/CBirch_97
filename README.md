# Description
This is my implementation of the CBirch_97 algorithm for head tracking

# Results
Here is an example of my algorithm at work

![Example of CBirch Tracking Algorithm](https://github.com/PeterJochem/CBirch_97/blob/master/CBirch97.gif "My Implemntation Results")

# How to Run my Code
To process the image set with sum of square errors, run ```python3 cbirch.py sse```. The resulting output is in a file called output_sum_square.avi. If any part of the frame leaves the image, then I choose to simply not display the frame.
 
To process the image set with cross correlation, run ```python3 cbirch.py cc```. The output is in a file called output_cc.avi. If any part of the frame leaves the image, then I choose to simply not display the bounding box. 

To process the image set with normalized cross correlation run ```python3 cbirch.py ncc```. The output is in a file called output_normalized_cc.avi



