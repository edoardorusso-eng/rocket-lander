# Rocket Lander

A simple 2D rocket landing simulator built with Python and Pygame.

The goal is to safely land the rocket on the landing pad while controlling thrust, rotation, horizontal speed, vertical speed, and fuel.

## Features

- Simple 2D rocket physics
- Gravity and thrust
- Rotational control
- Fuel consumption
- Landing pad detection
- Safe landing conditions
- Crash detection
- Explosion animation
- Restart system

## Controls

- `SPACE` — fire the main engine
- `A` — rotate left
- `D` — rotate right
- `R` — restart after landing or crashing

## Landing Conditions

A successful landing requires:

- landing on the pad
- low vertical speed
- low horizontal speed
- a nearly vertical rocket

Otherwise, the rocket crashes.

## Installation

Install Python and then install Pygame Community Edition:

```bash
python -m pip install pygame-ce

## Run

Open a terminal inside the project folder and run:
python rocket.py
