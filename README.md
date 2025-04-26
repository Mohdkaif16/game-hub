# Game Hub

## Overview

**Game Hub** is a Python-based game hub that allows users to play various classic games with a simple and interactive graphical user interface (GUI) built using **Tkinter** and **Pygame**. The game hub supports four games:

- Tic Tac Toe
- Snake
- Pong
- Memory Match (Flip Cards)

Additionally, players can toggle between light and dark themes, view their scores for each game, and play against AI in selected games.

## Features

- **Tic Tac Toe**: Play against another player or toggle AI to play against the computer.
- **Snake**: Control a snake to eat food and grow in size, while avoiding collisions with walls or the snake's own body.
- **Pong**: A classic Pong game with both player vs player and player vs AI modes.
- **Memory Match**: Flip cards to find matching pairs, play against another player or toggle AI for solo play.
- **Light/Dark Theme**: Toggle between light and dark themes for the GUI.
- **Score Tracking**: Keep track of your scores for each game, stored in a `scores.json` file.

## Requirements

Before running the project, ensure you have the following installed:

- Python 3.12
- Tkinter (comes pre-installed with Python)
- Pygame (for the games)

To install Pygame, run:

```bash
pip install pygame
