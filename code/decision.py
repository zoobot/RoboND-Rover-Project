import numpy as np
import random


# This is where you can build a decision tree for determining throttle, brake and steer
# commands based on the output of the perception_step() function
def decision_step(Rover):
    bias = 13
    side = 10
    turn = 15

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:

        # Check for Rover.mode status
        if Rover.mode == 'forward':

            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:
                Rover.count = 0
                print(' -- forward good terrain -- ',Rover.mode)
                # If mode is forward, navigable terrain looks good
                # and velocity is below max, then throttle
                if Rover.vel < Rover.max_vel:
                    print(' -- forward throttling to max -- ',Rover.mode)
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                    if Rover.vel == 0 and Rover.throttle == 0.2:
                        Rover.mode = 'stuck'
                else: # Else coast
                    print(' -- forward coasting -- ',Rover.mode)
                    Rover.throttle = 0
                # Set steering to average angle clipped to the range +/- 25
                Rover.brake = 0
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + bias, -side, side)

            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                print(' -- stopping because bad terrain -- ',Rover.mode)
                # Set mode to "stop" and hit the brakes!
                Rover.throttle = 0
                # Set brake to stored brake value
                Rover.brake = Rover.brake_set
                Rover.steer = 0
                Rover.mode = 'stop'


        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            print('stop',Rover.mode)
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                print('stop but moving so break',Rover.mode)
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                print('stopped totally check vision',Rover.mode)
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    print('stopped no vision so turn',Rover.mode)
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    Rover.steer = -turn # Could be more clever here about which way to turn

                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    print('stopped good vision so go forward',Rover.mode)
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) + bias, -side, side)
                    Rover.mode = 'forward'
        elif Rover.mode == 'stuck':
            # perc_mapped = Rover.perc_mapped #not sure this will work...
            print('-- reversing from stuck mode')

            Rover.throttle = Rover.max_vel
            while Rover.mode == 'stuck':
                Rover.count += 1
                if Rover.count > 10:
                    Rover.throttle = 0
                    Rover.steer = -turn
                    Rover.brake = 0
                    print('-- stuck still stop')
                    Rover.mode = 'donut'
                if Rover.mode == 'donut':
                    print('big fat donut',Rover.mode)
                    Rover.throttle = -Rover.throttle_set
                    Rover.brake = 0
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -side, side)
                    Rover.mode = 'stop'





    # Just to make the rover do something
    # even if no modifications have been made to the code
    else:
        print('do something!',Rover.mode)
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0

    if Rover.near_sample and not Rover.picking_up:
        Rover.send_pickup = True
        Rover.mode = 'stop'


    if Rover.send_pickup and Rover.picking_up:
        Rover.send_pickup = False
        # self.samples_pos = None # To store the actual sample positions
        # self.samples_found = 0 # To count the number of samples found
        # self.near_sample = 0 # Will be set to telemetry value data["near_sample"]
        # self.picking_up = 0 # Will be set to telemetry value data["picking_up"]
        # self.send_pickup = False # Set to True to trigger rock pickup


    if Rover.vel == 0.00 and Rover.throttle == Rover.max_vel:
        print('-- stuck')
        Rover.mode = 'stuck'
    # if Rover.vel == Rover.max_vel and :

    return Rover