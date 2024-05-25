# hypr-nerd-gestures

## Project Statement

I use the [Hyprland](https://github.com/hyprwm/Hyprland) compositor on my daily linux distro. I want to control the window position, workspace and other stuff in Hyprland using hand gestures. **This project uses AI to understand different gestures in real time from the webcam to call Hyperland functions**. Some example functions are:
- swipe right to move to the workspace on the right
- swipe left to move to workspace on the left
- raise one finger to move the cursor
- use two finger to adjust the volume
- others

This project will use OpenCV and python3

## Developement Environment

I highly suggest using nix developement environment to have a consistant environment. You can enter the environment with
```bash
nix develop
```

If you don't have nix, you need to have installed the following programs / libraries:
- python3
- opencv-python
