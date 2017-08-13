# tracking-cars-highway
Modified Lucas-Kanade algorithm to detect and track cars

cabrillo1.asf is the movie of cars to track

lk_track2.py is the modified Lucas-Kanade algorithm to track cars, features are detected using the Harris corner detection algorithm. The output is all the position and instantaneous velocity of features, as cabrillo-1-lk.txt

lk-linker_2 links the positions of cars plus instantaneous velocity to nearest positions in adjacent times through k-d-tree in order to build 'IDs' of cars. Output is cabrillo-1-lk-tracked.txt

lk-track-traj visualizes cabrillo-1-lk-tracked.txt to confirm tracking


Here's an example:

(./image/227.jpg)
