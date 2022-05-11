# technical_question 
As a precursor, this was a great technical question! I had a lot of fun experimenting with different networks and having a play with the results.
I do not own a CUDA enabled GPU, therefore my implementation runs through a Colab notebook -> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/17zqx4rOEP1035AjPfDE5JyaloIB06oq5?usp=sharing)
## Survey of current SOTA
The first phase of this question involved surveying the latest 3D human reconstruction networks, with the following conditions: 
- The input being a single  mp4 file.
- The output being a set of either 3D meshes or point clouds, ideally one for each frame.


I've worked previously with ONet, PIFu, LDIF, and NeRF networks. PIFuHD was my initial first guess at a potential solution to this question as it was trained for high-detail human reconstruction (including clothing). However, it is always worth a trip to google scholar to check the forward citations. Through this I was able to find ICON, released in Feb 2022. My reasons for selecting ICON as my chosen solution are as follows:
- ICON has a full, well documented codebase, with access to a plug-and-play Colab notebook for easy testing.
- The ICON paper demostrates results that consistantly outperform PIFu / PIFuHD, with particularly better generalisation to dramatic / athletic poses through use of local (rather than global) features.
In the next section I will give a high-level overview of the the theory behind ICON and its network architecture.
## ICON architecture rundown
![Image of ICON Network Architecture](https://icon.is.tue.mpg.de/media/upload/architecture.png)
The ICON architecture consists of two parts, with an optional optimisation loop:
1.  First, we create normal predictions for the front and back side of the human:
    - This involves inferring a SMPL-body mesh (denoted as ![equation](https://latex.codecogs.com/png.image?\dpi{110}\bg{white}M), provided by [PyMAF](https://hongwenzhang.github.io/pymaf/)) from the input image. 
    - Then, using a differentiable renderer (denoted as ![equation](https://latex.codecogs.com/png.image?\dpi{110}\bg{white}DR)), we obtain a front and back SMPL-body normal maps (denoted as ![equation](https://latex.codecogs.com/png.image?\dpi{110}\bg{white}N^b)).
    - Combining the SMPL-body normal maps with the original rgb image, ICON uses two trained normal prediction networks (denoted as ![equation](https://latex.codecogs.com/png.image?\dpi{110}\bg{white}G_N)) to infer front / back clothed-body normal maps.
2. (Optional) These predicted clothed-body normal maps can be further optimised by passing them through a refinement loop, where we itteratively minimise the difference between the rendered SMPL-body normal-maps and the predicted clothed-body normal maps.
3. When we have the final inferred clothed-body normal maps, we then predict occupancy for a query point P by feeding a local feature vector into an MLP. The local feature vector consists of:
    - The signed distance from P to the closest body point on the SMPL-body mesh.
    - The [barycentric surface normal](https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/barycentric-coordinates) of the closest body point on the SMPL-body mesh.
    - A normal vector extracted from either the front or the back inferred clothed-body normal map, depending on visability.

Using this architecture, we can begin building an [octree](https://iq.opengenus.org/octree/) by querying different points, which can then be converted to a mesh via marching cubes. 

## Results
[result](resources/videos/result.mp4)


## Advantages of ICON (Specific to Metacast)
- Pose Generalisation
    - Many of the datasets used to train human reconstruction networks (RenderPeople) are limited in pose variation. 
    - Past SOTA networks suffered when exposed to 'dramatic' poses as they utilised global image features (i.e. taking the whole image into account), which overfit to poses seen during training. 
    - In contrast, ICON uses local features (generated from a combination of pose estimation and normal map prediction), which allows for better generalisation to unseen poses.
    - As Metacast is attempting to reconstruct athletic / dynamic poses, ICON generates far more accurate results when compared to other SOTA networks. 
- Quality of output
    - Comparing directly to PIFu's architecture, the inclusion of a mesh-based statistical model (PyMAF) in ICON greatly reduces 'non-human' artifacts, at the expense of having a generic look to all outputs (further discussed in limitations section). This also combats the effect of image blur.
## Limitations of ICON (Specific to Metacast)
- The first obvious limitation - ICON is far from a real-time solution, standing at 30.7 seconds per frame. Through ommition of the normal map optimisation loop, the iteration time for a single frame was greatly reduced to 4.4s (using Colab's Tesla-P100 instances), with a noticible difference in quality.
- ICON is designed to work as a single image reconstructor, rather than a video reconstructor. As frames from the .mp4 are reconstructed individually, there is currently no consistency in scale / position between successive models. This could be rectified in the future by restructuring ICON to work as a recurrent network, where the output of each frame is conditioned on the output of previous frames.
- By using a pretrained mesh-based statistical model (PyMAF), the output mesh is currently limited to a single human. This means (1) No equiptment is reconstructed (2) Only single humans are reconstructed. From what I gathered in PyMAF's paper, to solve these problems new pose and shape estimation models would have to be trained for each sport. As a loose example, to reconstruct a fencing scene we would need to:
    - Alter PyMAFs SMPL models to include 2 people, and 2 swords.
    - Retrain PyMAF on annotated fencing data (i.e. pixel perfect positions for both people and both swords for each frame of training data). This would take a long time to implement!
- ICON reconstruction relies on PyMAF, which exposes it to PyMAF failure cases. In their words - "Though PyMAF can improve the alignment of some body parts, it remains challenging for PyMAF to correct those body parts with severe deviations, heavy occlusions, or ambuiguous limb connections."
    - For instance, occluded regions can sometimes cause missing limbs  
        <p float="left">
            <img src="resources/eval-images/missing_limbs/2.png" height="300" />
            <img src="resources/eval-images/missing_limbs/1.png" height="300" /> 
        </p>
    - 
    

- ICON assumes weak perspective cameras, which makes it succeptable to failure when subjects are close to the lens / distorted. In a UFC ring subjects might get very close to cameras.

## Improvements Made
The improvements that I mention in the limitations section are non trivial, and require a whole rework of the model and the training data. For this technical question, I will focus on mesh post-processing to obtain a smoother surface.

## A brief statement on how you would write a test suite for your video converter. e.g. how would you validate that your outputs are reasonable? 
- Unit Testing
    - 
- Converter Evaluation
    - At training time, I have found the best quantitative metric for evaluating outputs has been 3D IOU.
    - At test time, we have no ground truth model for 3D IOU calculations, therefore evaluation becomes more tricky.
    - However, if we could (1) output the inferred extrinsic camera coordinates and (2) line up the reconstruction silouette with the original video, we would then be able to run 2D IOU on the gt video segmentation vs the sillouette of the reconstruction (I believe ICON already uses this approach as a loss function).
    - This is still a poor way of measuring performance, as we're only using one view. The model could extend infinitely in the direction the camera is facing and still achieve a good score.
    - To tag an output as 'reasonable' you could use a 2D IOU threshold (e.g. 90%).
## Other Approaches
As a side note - if an output 3D mesh wasn't a requirement, recent NeRF networks (https://github.com/NVlabs/instant-ngp) would definitely catch my eye:
- NeRF networks train on a single scene, take camera coordinates as input and give 2D images as output.
- From a realism standpoint, the detail, color and material properties (reflections, roughness etc) of NeRF's 2D outputs far outpace 3D mesh generation networks, at the cost of having no output mesh to work with.
- Limitations:
    - This network requires a very beefy GPU and is prone to VRAM overflow related crashes.
    - This network requires multiple cameras to achieve good results, so the monocular video data provided withthis task wouldn't be usable. 