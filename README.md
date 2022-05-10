# technical_question

Paper research
	- PIFuHD
	- PyMAF (pose estimation)
	- ICON: Implicit Clothed humans Obtained from Normals 

Improvements
	- HoMer positioning

Possible problem areas
	- Blur
	- Background removal

A brief statement on how you would write a test suite for your video converter. 
e.g. how would you validate that your outputs are reasonable? 
	- This is a difficult question as, at test time, we have no ground truth model for 3D IOU calculations
	- However, if we could output the inferred extrinsic camera coordinates and line up the reconstruction with the original video, we would then be able to run 2D IOU on the  gt video vs the reconstruction.
		○ Using 2D human segmentation networks for gt video and 
	- To tag an output as 'reasonable' you could use a 2D IOU threshold from the perspective of the original camera. 
	- Otherwise, you could run a 3D pose estimation for (PyMAF) and use 3D IOU there.

