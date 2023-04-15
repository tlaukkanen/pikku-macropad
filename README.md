# Pikku - Raspberry Pi Pico Powered Macropad

This is a simple macropad built with Raspberry Pi Pico. See detailed description in my blog post at:

[codeof.me/pikku-raspberry-pi-pico-powered-macropad](https://codeof.me/pikku-raspberry-pi-pico-powered-macropad)

![Two macropads 3d printed with different colors](docs/Pikku_stack.jpg)

Macropad support different models which you can change by pressing the top left key. Other buttons can be customized to do different things. This initial code includes the following modes:

| Mode | Action | Key |
|---|---|---|
| **Microsoft Teams** | | |
| | Search | Key 2 |
| | Goto |       Key 3 |
| | Toggle mute | Key 4 |
| | Toggle camera | Key 5 |
| | Hangup | Key 6 |
| **VS Code** | | |
| | Explorer | Key 2 |
| | Problems | Key 3 |
| | Search | Key 4 |
| | Debug | Key 5 |
| | Output | Key 6 |
| **Git** | | |
| | Branch.. | Key 2 |
| | Checkout main | Key 3 |
| | Status | Key 4 |
| | Push | Key 5 |
| | Pull org main | Key 6 |

The active mode is displayed in a small SSD1306 display.

![Pikku macropad showing selected mode in display](docs/Pikku_display.jpg)

# Schematics

![Circuit diagram of the Pikku macropad](docs/Pikku_circuit.png)

# 3D Printed Case

Case is constructed of three parts. All parts can be printed without support. Parts snap-fit together without need for glue. STL files can be found from the [stl-files](stl-files/) folder.

![3D model of the Pikku macropad case](docs/Pikku_3D_case.png)
