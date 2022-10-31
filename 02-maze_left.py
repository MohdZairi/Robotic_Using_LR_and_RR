#!/usr/bin/env python3
from eye import *


# This left wall-following program is obviously INCOMPLETE
# TODO: Complete this LEFT wall-following program
# You are ALLOWED to refer to ANY references

SPEED = 80  # Original value: 360
ASPEED = 45
THRES = 176  # Original value: 176
NTHRES = 88  # 88

DISTANCE = 40  # Original value: 360
DEGREE_TO_TURN = 90  # ORI 100
DEGREE_TO_CURVE = 45


def turn_left():
    VWTurn(DEGREE_TO_TURN, ASPEED)  # turn
    VWWait()


# do checkout VWCurve() instead, refer the RoBIOS page
def turn_right():
    VWTurn(-DEGREE_TO_TURN, ASPEED)  # turn
    VWWait()


def straight():
    VWStraight(DISTANCE, SPEED)  # go one step
    VWWait()


def wall_right():
    VWCurve(DISTANCE, -50, SPEED)  # curve
    VWWait()


def wall_left():
    VWCurve(DISTANCE, 50, SPEED)  # curve
    VWWait()


def curve_left():
    VWCurve(DISTANCE, DEGREE_TO_CURVE, SPEED)  # curve
    VWWait()


def curve_right():
    VWCurve(DISTANCE, -DEGREE_TO_CURVE, SPEED)  # curve
    VWWait()


def main():
    LCDPrintf("My MAZE LEFT\n")
    LCDMenu("SCAN", "", "", "END")
    while KEYRead() != KEY4:
        min_scan = (THRES / 3)  # put a very high scan value (distance) initially at each step/scan, 15000 mm is 15 meters
        min_scan_index = 0  # initial (at each step/scan) index is 0, i.e. rear of robot
        heading_to_turn = 0  # initial (at each step/scan) heading to turn is 0 degree, i.e. no need to turn!
        scan = LIDARGet()

        for i in range(0, 360):  # read 360-degrees range around the robot
            LCDLine(i, 250 - int(scan[i] / 10), i, 250, BLUE)
            if scan[i] <= min_scan:
                LCDSetPrintf(
                    2, 45, "NEW min detected: %d mm\n", scan[i]
                )  # just to check the minimum reading
            min_scan = scan[i]
            min_scan_index = i

        # mark the minimum reading on the plot, using yellow line
        LCDLine(min_scan_index, 250 - int(min_scan / 10), min_scan_index, 250, YELLOW)

        front = int(PSDGet(PSD_FRONT) > THRES)
        left = int(PSDGet(PSD_LEFT) > THRES)
        right = int(PSDGet(PSD_RIGHT) > THRES)

        #         fwall = int(PSDGet(PSD_FRONT) > THRES / 3)
        rwall = int(PSDGet(PSD_RIGHT) > NTHRES)
        lwall = int(PSDGet(PSD_LEFT) > NTHRES)

        if left == 1:
            LCDPrintf("LEFT is SAFE, now turning left\n")
            curve_left()

            if front == 1:
                LCDPrintf("FRONT is SAFE, now moving forward\n")
                straight()

        elif front == 1 & right == 1:
            LCDPrintf("FRONT and RIGHT is SAFE, now moving forward\n")
            if rwall == 0:
                LCDPrintf("FRONT is SAFE but RIGHT too CLOSE , now curve left\n")
                wall_left()
                if front == 1:
                    LCDPrintf("FRONT is SAFE, now moving forward\n")
                    straight()

            elif lwall == 0:
                LCDPrintf("FRONT is SAFE but LEFT too CLOSE , now curve right\n")
                wall_right()
                if front == 1:
                    LCDPrintf("FRONT is SAFE, now moving forward\n")
                    straight()

            else:
                straight()

        elif front == 1:
            if rwall == 0:
                LCDPrintf("FRONT is SAFE but RIGHT too CLOSE , now curve left\n")
                wall_left()

            elif lwall == 0:
                LCDPrintf("FRONT is SAFE but LEFT too CLOSE , now curve right\n")
                wall_right()

            else:
                LCDPrintf("FRONT is SAFE, now moving forward\n")
                straight()

        elif right == 1:
            LCDPrintf("RIGHT is SAFE, now turning right\n")
            straight()
            turn_right()
            if rwall == 0:
                LCDPrintf("FRONT is SAFE but RIGHT too CLOSE , now curve left\n")
                wall_left()

            elif lwall == 0:
                LCDPrintf("FRONT is SAFE but LEFT too CLOSE , now curve right\n")
                wall_right()

            else:
                LCDPrintf("FRONT is SAFE, now moving forward\n")
                straight()
        else:
            LCDPrintf("LEFT, FRONT and RIGHT are NOT safe, turning back on the spot\n")
            turn_left()  # all are not safe, now turning around
            turn_left()  # to achieve 180 turn around

    return 0


if __name__ == "__main__":
    main()
