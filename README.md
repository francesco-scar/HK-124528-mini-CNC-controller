# HK-124528 Mini-CNC controller - Arduino interface

I created this repository just to save somewhere some documentation about the HK-124528 CNC driver board, because at the time I'm writing this I wasn't able to find information about this specific board, so there is no code in this repo, but just text and images.

## Disclaimer

Everything wrote here come just from my experience, so it could be wrong, please double-check everything before try that out. Anyway, I'm not responsable for any damage. Thanks.

## Introduction

The HK-124528 is a board that takes as input from the parallel port connector the signals of steps and direction for each of the 3 stepper motors. At each pulse of the step data line the board send the current to the relative motor in order to make it step once in the direction specified by the direction data line (eg. 0V --> Clockwise; 5V --> Counterclockwise, but it depends by the motor's coils connections)

## Parallel port connections

From here on I will number parallel port pins accordingly to the standard parallel port pin numeration (as shown in this Wikipedia image, By AndrewBuck - Own work, CC BY-SA 3.0 [click here for more information](https://commons.wikimedia.org/w/index.php?curid=2565019))
![Parallel port pin](https://github.com/francesco-scar/HK-124528-mini-CNC-controller/blob/main/images/800px-25_Pin_D-sub_pinout.svg)

I found out the following connections:

| Pin | Circuit path | Function | Additional connections on board |
|:---:|:------------:|:--------:|:-------------------------------:|
|1|Not tested|||
|2|Schmitt-Trigger Inverts(7414) -> Controlled Buffer (74125) -> Optocoupler|X Step|Not Tested|
|3|Schmitt-Trigger Inverts(7414) -> Controlled Buffer (74125) -> Optocoupler|X Dir|Not Tested|
|4|Schmitt-Trigger Inverts(7414) -> Controlled Buffer (74125) -> Optocoupler|Y Step|CN8 CLK+|
|5|Schmitt-Trigger Inverts(7414) -> Controlled Buffer (74125) -> Optocoupler|Y Dir|CN8 CLK+|
|6|Schmitt-Trigger Inverts(7414) -> Controlled Buffer (74125) -> Optocoupler|Z Step|CN8 CLK+|
|7|Schmitt-Trigger Inverts(7414) -> Controlled Buffer (74125) -> Optocoupler|Z Dir|CN8 CLK+|
|8|Not tested|||
|9|Not tested|||
|10|Not tested|||
|11|Not tested|||
|12|Not tested|||
|13|Not tested|||
|14|Buffer (74125) control pin|Power and enable stepper|Not Tested|
|15|Not tested|||
|16|Not tested|||
|17|Not tested|||

This is still a work in progress...
