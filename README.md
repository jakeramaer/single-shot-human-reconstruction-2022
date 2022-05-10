# technical_question

## TO DO
- Summarise ICON
- Build functionality for mp4 -> png conversion

As a precursor, this was a great technical question! I had a lot of fun experimenting with different networks and having a play with the results. \
I do not own a CUDA enabled GPU, so most of this work was completed using Google Colab.

## Survey of current SOTA
The first phase of this question involved surveying the latest 3D human reconstruction networks, with the following conditions: 
- The input being a single  mp4 file.
- The output being a set of either 3D meshes or point clouds, ideally one for each frame.

I've worked previously with ONet, PIFu, LDIF, and NeRF networks. PIFuHD was my initial first guess at a potential solution to this question as it was trained for high-detail human reconstruction (including clothing). However, it is always worth a trip to google scholar to check the forward citations. Through this I was able to find ICON, released in Feb 2022. My reasons for selecting ICON as my chosen solution are as follows:
- ICON has a full, well documented codebase, with access to a plug-and-play Colab notebook for easy testing.
- The ICON paper demostrates results that consistantly outperform PIFuHD, with particularly better generalisation to dramatic / athletic poses through use of local (rather than global) features.

In the next section I will give a high-level overview of the the theory behind ICON and its network architecture.

## ICON rundown
the ICON network works like this...

## Limitations of ICON
- Human only, no equiptment (this can most likely be changed)
- Blur
- Background removal
- Multiple people (test this!)

## 



Paper research
	- ONet (old faithful)
    - PIFuHD
	- ICON: Implicit Clothed humans Obtained from Normals 

Improvements
	- HuMoR / FLAG pose estimation, rather than PARE.


## A brief statement on how you would write a test suite for your video converter. e.g. how would you validate that your outputs are reasonable? 

- This is a difficult question as, at test time, we have no ground truth model for 3D IOU calculations
- However, if we could output the inferred extrinsic camera coordinates and line up the reconstruction with the original video, we would then be able to run 2D IOU on the  gt video vs the reconstruction (this is still a bad way to measure performance, as we're only using one view)
- To tag an output as 'reasonable' you could use a 2D IOU threshold from the perspective of the original camera. 
- Otherwise, you could run a 3D pose estimation for (PyMAF) and use 3D IOU there.

## Other Approaches
As a side note - if an output 3D mesh wasn't a requirement, recent NeRF networks (https://github.com/NVlabs/instant-ngp) would definitely catch my eye:
- NeRF networks train on a single scene, take camera coordinates as input and give 2D images as output.
- From a realism standpoint, the detail, color and material properties (reflections, roughness etc) of NeRF's 2D outputs far outpace 3D mesh generation networks, at the cost of having no output mesh to work with.
- Limitations:
    - This network requires a very beefy GPU and is prone to crashes.
    - This network requires multiple cameras to achieve good results (check this again), so the monocular video data wouldn't 

