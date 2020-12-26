# HK-124528 Mini-CNC controller - Arduino interface

I created this repository just to save somewhere some documentation about the HK-124528 CNC driver board, because at the time I'm writing this I wasn't able to find information about this specific board, so there is no code in this repo, but just text and images.

## Disclaimer

Everything wrote here come just from my experience, so it could be wrong, please double-check everything before try that out. Anyway, I'm not responsable for any damage. Thanks.

## Introduction

The HK-124528 is a board that takes as input from the parallel port connector the signals of steps and direction for each of the 3 stepper motors. At each pulse of the step data line the board send the current to the relative motor in order to make it step once in the direction specified by the direction data line (eg. 0V --> Clockwise; 5V --> Counterclockwise, but it depends by the motor's coils connections)

This is still a work in progress...
