# Face Swapping

This notebook is a small extract from the udacity AI computer vision course and demonstrates the ability to swap faces using numpy, dlib and OpenCV. (Original article on [reddit](https://www.reddit.com/r/programming/comments/3f591x/so_i_wrote_a_script_that_swaps_peoples_faces_in/) by Matthew Earl)

Note: The sample images are downloaded from wikimedia.org (see the attached license file). Code and notebook are MIT License.

The transformation process can be break down into four steps:

1. Detecting facial landmarks using _dlib_

<table><tr><td><img src="./generated/annotated_Andrea_V.jpg" alt="annotated sample 1" style="height: 320px;"/></td>
<td><img src="./generated/annotated_The_Equestrian_Session.jpg" alt="annotated sample 2" style="height: 320px;"/></td></tr></table>

## 2. Align faces with a procrustes analysis

<table><tr><td><img src="./Andrea_V.jpg" alt="annotated sample 1" style="height: 320px;"/></td>
<td><img src="./generated/warped_The_Equestrian_Session.jpg" alt="annotated sample 2" style="height: 320px;"/></td></tr></table>

## 3. Blending face features together

<table><tr><td><img src="./generated/masked_Andrea_V.jpg" alt="masked sample 1" style="height: 320px;"/></td>
<td><img src="./generated/combined_Andrea_V.jpg" alt="merged face sample 1" style="height: 320px;"/></td></tr></table>

## 4. Color correction and final output

<table><tr><td><td><img src="./generated/debug2_Andrea_V.jpg" alt="color corrected sample 2" style="height: 320px;"/></td>
<td><img src="./generated/final_Andrea_V.jpg" alt="final face sample 1" style="height: 320px;"/></td></tr></table>

Further instructions can be found in the notebook.