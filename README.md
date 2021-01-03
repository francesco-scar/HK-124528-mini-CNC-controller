# HK-124528 Mini-CNC controller - Arduino interface

I created this repository just to save somewhere some documentation about the HK-124528 CNC driver board, because at the time I'm writing this I wasn't able to find information about this specific board, so there is no code in this repo, but just text and images.

## Disclaimer

Everything wrote here come just from my experience, so it could be wrong, please double-check everything before try that out. Anyway, I'm not responsable for any damage. Thanks.

## Introduction

The HK-124528 is a board that takes as input from the parallel port connector the signals of steps and direction for each of the 3 stepper motors. At each pulse of the step data line the board send the current to the relative motor in order to make it step once in the direction specified by the direction data line (eg. 0V --> Clockwise; 5V --> Counterclockwise, but it depends by the motor's coils connections).
I used the [grbl](https://github.com/grbl/grbl) firmware (Version 1.1, but other versions should work as well) on an Arduino Uno board to control the driver.

## Parallel port connections

From here on I will number parallel port pins accordingly to the standard parallel port pin numeration (as shown in this Wikipedia image, By AndrewBuck - Own work, CC BY-SA 3.0 [click here for more information](https://commons.wikimedia.org/w/index.php?curid=2565019))
![Parallel port pin](https://github.com/francesco-scar/HK-124528-mini-CNC-controller/blob/main/images/800px-25_Pin_D-sub_pinout.svg)

I found out the following connections:

| Pin | Circuit path | Function | Additional connections on board |
|:---:|:------------:|:--------:|:-------------------------------:|
|1|Not tested|||
|2|Schmitt-Trigger Inverts(7414) -> Controlled Buffer (74125) -> Optocoupler|X Step|CN7 CLK+|
|3|Schmitt-Trigger Inverts(7414) -> Controlled Buffer (74125) -> Optocoupler|X Dir|CN7 CW+|
|4|Schmitt-Trigger Inverts(7414) -> Controlled Buffer (74125) -> Optocoupler|Y Step|CN8 CLK+|
|5|Schmitt-Trigger Inverts(7414) -> Controlled Buffer (74125) -> Optocoupler|Y Dir|CN8 CW+|
|6|Schmitt-Trigger Inverts(7414) -> Controlled Buffer (74125) -> Optocoupler|Z Step|CN10 CLK+|
|7|Schmitt-Trigger Inverts(7414) -> Controlled Buffer (74125) -> Optocoupler|Z Dir|CN10 CW+|
|8|Not tested|||
|9|Not tested|||
|10|Avalable|In my case used for emergency button|P10 on CN13|
|11|Not tested|||
|12|Not tested|||
|13|Not tested|||
|14|Buffer (74125) control pin|Power and enable stepper|Not Tested|
|15|Not tested|||
|16|Not tested|||
|17|Not tested|||

## Arduino Uno Connections

I connected the pins above to the Arduino Uno accordingly to their function; in the [grbl source](https://github.com/grbl/grbl/blob/master/grbl/cpu_map/cpu_map_atmega328p.h) code there are those definitions for pins:

```
// Define step pulse output pins. NOTE: All step bit pins must be on the same port.
#define STEP_DDR        DDRD
#define STEP_PORT       PORTD
#define X_STEP_BIT      2  // Uno Digital Pin 2
#define Y_STEP_BIT      3  // Uno Digital Pin 3
#define Z_STEP_BIT      4  // Uno Digital Pin 4
#define STEP_MASK       ((1<<X_STEP_BIT)|(1<<Y_STEP_BIT)|(1<<Z_STEP_BIT)) // All step bits

// Define step direction output pins. NOTE: All direction pins must be on the same port.
#define DIRECTION_DDR     DDRD
#define DIRECTION_PORT    PORTD
#define X_DIRECTION_BIT   5  // Uno Digital Pin 5
#define Y_DIRECTION_BIT   6  // Uno Digital Pin 6
#define Z_DIRECTION_BIT   7  // Uno Digital Pin 7
#define DIRECTION_MASK    ((1<<X_DIRECTION_BIT)|(1<<Y_DIRECTION_BIT)|(1<<Z_DIRECTION_BIT)) // All direction bits

// Define stepper driver enable/disable output pin.
#define STEPPERS_DISABLE_DDR    DDRB
#define STEPPERS_DISABLE_PORT   PORTB
#define STEPPERS_DISABLE_BIT    0  // Uno Digital Pin 8
```

You can change them if you want, but you have to pay attention (as said in the comments) that `All step/direction bit pins must be on the same port`.

I made this connections:

| Parallel Pin | Function | Arduino Pin |
|:------------:|:--------:|:-----------:|
|1|-|-|
|2|X Step|2|
|3|X Dir|5|
|4|Y Step|3|
|5|Y Dir|6|
|6|Z Step|4|
|7|Z Dir|7|
|8|-|-|
|9|-|-|
|10|Emergency button|A0|
|11|-|-|
|12|-|-|
|13|-|-|
|14*|Power and enable stepper*|GND|
|15|-|-|
|16|-|-|
|17|-|-|
|-|Z Probe|A5|
|GND|GND|GND|

\* you can connect this pin to pin 8, so that the steppers are enabled only when they have to turn, but I prefered keep them always active to avoid unwanted movements (and position loss), this way it consume more current and motors and drivers can heat up a little more, but otherwise the motors don't oppose resistance to unwanted forces along the axis.

This is still a work in progress...
