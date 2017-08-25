import numpy as np
import cv2

# Identify pixels above the threshold
# Threshold of RGB > 160 does a nice job of identifying ground pixels only
# def color_thresh(img, rgb_thresh):
#     # Create an array of zeros same xy size as img, but single channel
#     color_select = np.zeros_like(img[:,:,0])
#     # Require that each pixel be above all three threshold values in RGB
#     # above_thresh will now contain a boolean array with "True"
#     # where threshold was met
#     above_thresh = (img[:,:,0] > rgb_thresh[0])  \
#                 & (img[:,:,1] > rgb_thresh[1]) \
#                 & (img[:,:,2] > rgb_thresh[2])
#     # Index the array of zeros with the boolean array and set to 1
#     color_select[above_thresh] = 1
#     # Return the binary image
#     return color_select

def color_thresh(img, rgb_thresh_low, rgb_thresh_high):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:,:,0])
    # Require that each pixel be above all three threshold values in RGB
    # above_thresh will now contain a boolean array with "True"
    # where threshold was met
    above_thresh = (img[:,:,0] > rgb_thresh_low[0]) & (img[:,:,0] <= rgb_thresh_high[0]) \
                & (img[:,:,1] > rgb_thresh_low[1]) & (img[:,:,1] <= rgb_thresh_high[1])\
                & (img[:,:,2] > rgb_thresh_low[2]) & (img[:,:,2] <= rgb_thresh_high[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    # Return the binary image
    return color_select


# Define a function to convert to rover-centric coordinates
def rover_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the
    # center bottom of the image.
    x_pixel = np.absolute(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[0]).astype(np.float)
    return x_pixel, y_pixel


# Define a function to convert to radial coords in rover space
def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle)
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # Calculate angle away from vertical for each pixel
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles

# Define a function to apply a rotation to pixel positions
def rotate_pix(xpix, ypix, yaw):
    # TODO:
    # Convert yaw to radians
    # yaw_rad = yaw * np.pi / 180
    yaw_rad = np.radians(yaw)
    # Apply a rotation
    xpix_rotated = xpix * np.cos(yaw_rad) - ypix * np.sin(yaw_rad)
    ypix_rotated = xpix * np.sin(yaw_rad) + ypix * np.cos(yaw_rad)
    # Return the result
    return xpix_rotated, ypix_rotated

# Define a function to perform a translation
def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale):
    # TODO:
    # Apply a scaling and a translation
    xpix_translated = np.int_(xpos + (xpix_rot / scale))
    ypix_translated = np.int_(ypos + (ypix_rot / scale))
    # Return the result
    return xpix_translated, ypix_translated

# Define a function to apply rotation and translation (and clipping)
# Once you define the two functions above this function should work
def pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale):
    # Apply rotation
    xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
    # Apply translation
    xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
    # Perform rotation, translation and clipping all at once
    x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)
    # Return the result
    return x_pix_world, y_pix_world

# Define a function to perform a perspective transform
def perspect_transform(img, src, dst):
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    mask = cv2.warpPerspective(np.ones_like(img[:,:,0]), M, (img.shape[1], img.shape[0])) # make a mask of 1s
    return warped, mask
    # return warped

# Apply the above functions in succession and update the Rover state accordingly
def perception_step(Rover):
    # Perform perception steps to update Rover()
    # TODO:
    # NOTE: camera image is coming to you in Rover.img
    # 1) Define source and destination points for perspective transform
    dst_size = 5
    bottom_offset = 6
    source = np.float32([[14,140],[301,140],[200,96],[118,96]])
    destination = np.float32([[Rover.img.shape[1]/2 - dst_size, Rover.img.shape[0] - bottom_offset],
                      [Rover.img.shape[1]/2 + dst_size, Rover.img.shape[0] - bottom_offset],
                      [Rover.img.shape[1]/2 + dst_size, Rover.img.shape[0] - 2*dst_size - bottom_offset],
                      [Rover.img.shape[1]/2 - dst_size, Rover.img.shape[0] - 2*dst_size - bottom_offset],
                      ])

    # 2) Apply perspective transform
    warped, mask = perspect_transform(Rover.img, source, destination)
    # warped = perspect_transform(Rover.img, source, destination)

    # 3) Apply color threshold to identify navigable terrain/obstacles/rock samples
    navigation_map = color_thresh(warped, (160, 160, 160),(255, 255, 255))
    # obstacle_map = color_thresh(warped,(15, 15, 15),(89, 81, 75))
    rock_map  = color_thresh(warped,(110,110,18),(255, 255, 19))
    obstacle_map = np.absolute(np.float32(navigation_map) - 1) * mask

    # plt.imshow(threshed, smap='gray')

    # 4) Update Rover.vision_image (this will be displayed on left side of screen)

    Rover.vision_image[:,:,2] = navigation_map *255
    Rover.vision_image[:,:,1] = rock_map *255
    Rover.vision_image[:,:,0] = obstacle_map *255



    # 5) Convert map image pixel values to rover-centric coords
    xpix_nav, ypix_nav = rover_coords(navigation_map) # Convert to rover-centric coords
    xpix_obstacle, ypix_obstacle = rover_coords(obstacle_map)
    xpix_rock, ypix_rock = rover_coords(rock_map)


    # 6) Convert rover-centric pixel values to world coordinates
    # Generate 200 x 200 pixel worldmap
    # Rover.worldmap = np.zeros((200, 200, 3))

    # Rover.worldmap = Rover.worldmap.shape[0]
    scale = 2 * dst_size
    xpos,ypos = Rover.pos
    yaw = Rover.yaw
    # output image for navigation
    nav_x_world, nav_y_world = pix_to_world(xpix_nav, ypix_nav, xpos, ypos, yaw, Rover.worldmap.shape[0], scale)
    # output image for obstacles
    obstacle_x_world, obstacle_y_world = pix_to_world(xpix_obstacle, ypix_obstacle, xpos, ypos, yaw, Rover.worldmap.shape[0], scale)
    # output image for rocks
    rock_x_world, rock_y_world = pix_to_world(xpix_rock, ypix_rock, xpos, ypos, yaw, Rover.worldmap.shape[0], scale)



    # 7) Update Rover worldmap (to be displayed on right side of screen)
    # Get navigable pixel positions in world coords

    Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 1
    # Blue channel Navigation
    Rover.worldmap[nav_y_world, nav_x_world, 2] += 10
    Rover.worldmap[rock_y_world, rock_x_world, 1] += 1

    Rover.worldmap[:,:,:] = np.clip(Rover.worldmap[:,:,:],0,255)


    # 8) Convert rover-centric pixel positions to polar coordinates
    # Update Rover pixel distances and angles
    dists, angles = to_polar_coords(xpix_nav, ypix_nav)
    Rover.nav_angles = angles
    Rover.nav_dists = dists




    return Rover