# Square Pad

A small but versatile macropad!

<img alt="3D render of Square Pad" src="https://github.com/user-attachments/assets/1c3fc36b-7864-4a4f-82b6-af2328ff27e2" width="300" />
<img alt="3D outline of Square Pad" src="https://github.com/user-attachments/assets/c0fb86a1-a7d9-4ad5-b48d-160b647bb15c" width="300" />

Square pad is a KMK-powered, 8-key macropad with a rotary encoder, OLED display, and underglow lighting.  
It's inspired by the [Ocreeb MK2](https://github.com/sb-ocr/ocreeb-mk-2/tree/main) and was built for the [Hackpad](https://hackpad.hackclub.com/) program.

### Profile switching

The Square Pad can store and switch between several profiles, adapting the 8 keys and rotary encoder to whatever you need.  
To switch between presets, click the rotary encoder, rotate it to select a profile (shown on the OLED screen), and click to confirm. The underglow lighting will change colors, letting you know the current profile at a glance.

# Design

This is my first time designing a macropad/keyboard! Tons of Googling and bugging others here and there, but I (hopefully) did it!

## PCB

A total of 0 vias are on the PCB, ignoring THT and mounting holes. (there's no benefit to this, don't ask why)

<img alt="Schematic of the Square Pad PCB" src="https://github.com/user-attachments/assets/f1661084-6216-4a05-bc79-a689476b5d73" width="600" />

<img alt="Layout of the Square Pad PCB" src="https://github.com/user-attachments/assets/01ee51a5-0c14-46c7-97fd-414cb924b758" width="600" />

The PCB was designed in KiCad

## Case

The entire case can be 3D printed in 3 parts and assembled only with 6 M2x16mm screws and a tiny bit of hot glue for the screen. Each part is optimized for printability and quality with almost no supports.

<img alt="3D exploded view of Square Pad" src="https://github.com/user-attachments/assets/5af281df-3069-46fa-ad86-8b2b6c4085ad" width="300" />

The case was designed in Onshape

## Firmware

Square Pad is powered by custom firmware written with [KMK](https://github.com/KMKfw/kmk_firmware). The custom firmware enabled easy profile switching and configuration.

# BOM

Everything you need to make your own Square Pad, minus the solder, glue, sweat, and tears.

## Electronics

- 1x XIAO RP2040 (with headers)
- 1x EC11E Rotary Encoder (with switch)
- 1x Rotary Encoder Knob
- 1x 0.91" OLED Display
- 8x Cherry MX Switches
- 8x Blank DSA Keycaps
- 9x Diode (THT)
- 12x SK6812 Mini LEDs
- Wires (for display)

## Case

- 6x M2x16mm Screw
- 1x case_top.stl
- 1x case_mid.stl
- 1x case_btm.stl
- 4x 10mm Rubber Feet (or just use hot glue)
