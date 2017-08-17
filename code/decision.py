import numpy as np
import random


# This is where you can build a decision tree for determining throttle, brake and steer
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    if Rover.nav_angles is not None:
        if Rover.vel == 0.00 and Rover.throttle != 0:
            print('-- stuck -- ')
            Rover.mode = 'reverse'


        if Rover.mode == 'reverse':
            #stop
            # Rover.throttle = 0
            # Rover.brake = Rover.brake_set
            # Rover.mode = "stop"
            #reverse
            print('-- reversing from stuck mode -- ')

            Rover.throttle = -0.5
            Rover.vel = -Rover.max_vel #reverse
            Rover.mode == 'forward'
            if Rover.start_time - Rover.start_time <= 2.01:
                Rover.steer = -5
                Rover.mode = 'stop'


        # Check for Rover.mode status
        if Rover.mode == 'forward':

            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:
                print(' -- forward good terrain -- ',Rover.mode)
                # If mode is forward, navigable terrain looks good
                # and velocity is below max, then throttle
                if Rover.vel < Rover.max_vel:
                    print(' -- forward throttling to max -- ',Rover.mode)
                    # Set throttle value to throttle setting
                    Rover.steer = 0
                    Rover.throttle = Rover.throttle_set
                    Rover.vel = Rover.max_vel
                else: # Else coast
                    print(' -- forward coasting -- ',Rover.mode)
                    Rover.throttle = 0
                    Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
                    # Rover.steer = 2
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -17, 21)
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                print(' -- stopping because bad terrain -- ',Rover.mode)
                # Set mode to "stop" and hit the brakes!
                Rover.throttle = 0
                # Set brake to stored brake value
                Rover.brake = Rover.brake_set
                # Rover.steer = -15
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
                    # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
                    # Rover.steer = 15 # Could be more clever here about which way to turn
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    print('stopped good vision so go forward',Rover.mode)
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -20, 15)
                    Rover.mode = 'forward'



    # Just to make the rover do something
    # even if no modifications have been made to the code
    else:
        print('do something!',Rover.mode)
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0

    return Rover

