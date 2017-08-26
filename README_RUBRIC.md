## Project: Search and Sample Return


---

** Setup/Notes
* conda info --envs #show the envs
* conda create -n testEnv python=3.5 # create environmet
# activate the environment
* source activate testEnv
* jupyter notebook starts the jupyter notebook
* python drive_rover.py starts the Rover driving in Unity Engine


**The goals / steps of this project are the following:**
* Goal is to get Rover driving autonomously and find and pickup rocks
* Set up mini-conda environment for python code
* Complete all Training in Jupyter Notebook
* Record Video
* Install Unity Engine Simulator
* Drive Rover with python via Unity Engine
* Map at least 40% of the environment with 60% fidelity
* Find at least 1 rock

**Training / Calibration**

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook).
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands.
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.

---
### Writeup / README


### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
Here is an example of how to include an image in your writeup.

![Grid Threshed][image4]: ./calibration_images/grid_threshed.jpg

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result.
And another!

![Right Side Nav][image5]:./calibration_images/right_side_nav.jpg

### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.

*Comments

**Screen Resolution: 1024x768
**Graphics Quality: Good
**FPS: 15

#### Rover is a basic wall follower with a bias of 13 and a side to side range of motion of -10/10.
I gave the thresh a range so I could use the color thresh function for rocks too. Used a mask for the obstacles.

* Issues
#### Rover still gets stuck in loop and on obstacles sometimes.
It picks up rocks if they are right in front of it.
Wouold like to figure out way to eliminate area that it's already travelled.
Stops following left wall if the curve is too large or if the Rover is pointing the wrong way when it goes around some turns.



