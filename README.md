This is my implementation of the CBIRCH_97 algorithm for head tracking
The image processing is quite slow. If you would like to run my code to generate the results given above, then do the following: 
To process the image set with sum of square errors, run python3 cbirch.py sse. The resulting output is in a file called output_sum_square.avi. If any part of the frame leaves the image, then I choose to simply not display the frame. 
To process the image set with cross correlation, run python3 cbirch.py cc. The output is in a file called output_cc.avi. If any part of the frame leaves the image, then I choose to simply not display the bounding box. 
To process the image set with normalized cross correlation run python3 cbirch.py ncc. The output is in a file called output_normalized_cc.avi



