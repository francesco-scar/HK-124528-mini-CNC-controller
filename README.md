# HK-124528 Mini-CNC controller - Arduino interface

I created this repository just to save somewhere some documentation about the HK-124528 CNC driver board, because at the time I'm writing this I wasn't able to find information about this specific board, so there is no code in this repo, but just text and images.

## Table of contents

- [Disclaimer](#Disclaimer)
- [Introduction](#Introduction)
- [Parallel port connections](#Parallel-port-connections)
- [Arduino Uno Connections](#Arduino-Uno-Connections)
- [Flash firmware on Arduino Uno](#Flash-firmware-on-Arduino-Uno)
- [Universal G-Code Sender (UGS)](#Universal-G-Code-Sender-UGS)
- [Parameters configuration](#Parameters-configuration)
- [Dip Switches](#Dip-Switches)

## Disclaimer

Everything wrote here come just from my experience, so it could be wrong, please double-check everything before try that out. Anyway, I'm not responsable for any damage. Thanks.

## Introduction

![Board Layout Top](https://github.com/francesco-scar/HK-124528-mini-CNC-controller/blob/main/images/20201224_121057_edit.jpg)

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
|CN7 CLK+ (2)\*|X Step|2|
|3|X Dir|5|
|CN8 CLK+ (4)\*|Y Step|3|
|5|Y Dir|6|
|CN10 CLK+ (6)\*|Z Step|4|
|7|Z Dir|7|
|8|-|-|
|9|-|-|
|10|Emergency button \*\*|A0|
|11|-|-|
|12|-|-|
|13|-|-|
|14*|Power and enable stepper\*\*\*|GND|
|15|-|-|
|16|-|-|
|17|-|-|
|-|Z Probe|A5|
|GND|GND|GND|

\* I connected those right before the optocoupler, after the controlled buffer output, because, for some reason, if I connect both step and dir signal to the parallel port the motors loose steps, otherwise with both after the buffer the motors turn only in one direction or not work at all (but could be a problem of the board I tested and both on parallel port could work for you, just try it if you want).

\*\* **ATTENTION:** The emergency stop is handled in software, in my case, so test it consistently before regular use of the CNC, because the false safe-feeling of it can be really dangerous in an emergency situation. In addition to this, in my case, the spindle has a separate driver circuit and is manually controlled by a switch and a potentiometer, so the emergency button will **NOT** stop it and the spindle will continue to rotate, pay attention to that too.

\*\*\* you can connect this pin to pin 8, so that the steppers are enabled only when they have to turn, but I prefered keep them always active to avoid unwanted movements (and position loss), this way it consume more current and motors and drivers can heat up a little more, but otherwise the motors don't oppose resistance to unwanted forces along the axis.

## Flash firmware on Arduino Uno

To flash the GRBL firmware you can just download it from [their repository](https://github.com/grbl/grbl) and open the /grbl/examples/grblUpload/grblUpload.ino file in the Arduino IDE and upload it on the board (as any other Arduino sketch).

Note: I don't have any credits for the grbl firmware, I'm just a normal user, they and their community did all the work :-)

## Universal G-Code Sender (UGS)

The easyest way, in my opinion, to send send the g-code instructions to your grbl controlled CNC is using the universal g-code sender and you can find information about installation and usage on the [UGS github repository](https://github.com/winder/Universal-G-Code-Sender).

To test that everything works so far you can just connect your arduino to the PC using a USB cable, launch UGS and choose the right port from the drop-down menu. Select the right baud-rate (the default one is 115200) and click the connect icon. When the connection is established you can move the machine using the jog window.

Note: Again, I don't have any credits for the UGS software, I'm just a normal user, they and their community did all the work :-)

## Parameters configuration

Sending the command ```$$``` to the arduino you can see the current grbl parameters values and you can change them with ```$param=val``` eg. ```$100=400.0```

Those settings worked for me:

```
$0 = 10    (step pulse, usec)
$1 = 25    (step idle delay, msec)
$2 = 0    (step port invert mask:00000000)
$3 = 6    (dir port invert mask:00000110)				<-- EDITED
$4 = 0    (step enable invert, bool)
$5 = 0    (limit pins invert, bool)
$6 = 0    (probe pin invert, bool)
$10 = 3    (status report mask:00000011)
$11 = 0.010    (junction deviation, mm)
$12 = 0.002    (arc tolerance, mm)
$13 = 0    (report inches, bool)
$20 = 0    (soft limits, bool)
$21 = 0    (hard limits, bool)
$22 = 0    (homing cycle, bool)
$23 = 0    (homing dir invert mask:00000000)
$24 = 25.000    (homing feed, mm/min)
$25 = 500.000    (homing seek, mm/min)
$26 = 250    (homing debounce, msec)
$27 = 1.000    (homing pull-off, mm)
$100 = 400.000    (x, step/mm)							<-- EDITED
$101 = 400.000    (y, step/mm)							<-- EDITED
$102 = 400.000    (z, step/mm)							<-- EDITED
$110 = 500.000    (x max rate, mm/min)
$111 = 500.000    (y max rate, mm/min)
$112 = 500.000    (z max rate, mm/min)
$120 = 10.000    (x accel, mm/sec^2)
$121 = 10.000    (y accel, mm/sec^2)
$122 = 10.000    (z accel, mm/sec^2)
$130 = 200.000    (x max travel, mm)
$131 = 200.000    (y max travel, mm)
$132 = 200.000    (z max travel, mm)

```

In particular you can calculate the step/mm parameter moving the wanted axis of a length ```L```, measuring the actual distance travelled ```D``` and given the ```OLD``` value of this setting you can get the ```NEW``` one using the formula ```NEW = (L/D)*OLD```. Otherwise you can calculate this value from the screw pitch.



## Dip Switches

![Dip Switches status](https://github.com/francesco-scar/HK-124528-mini-CNC-controller/blob/main/images/20201230_113053_edit.jpg)

The dip switches on the board allows you to set the current limit (SW1 and SW2), decade mode (SW3 and SW4) and microstepping (SW5 and SW6) for the stepper driver.
After some tries and errors I think the best combination in my case was the one showed in the image above.

This is still a work in progress...
