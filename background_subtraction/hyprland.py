from hyprpy import Hyprland

instance = Hyprland()

def move_workspace_left():
    instance.command_socket.send_command("dispatch", args=["workspace", "-1"])

def move_workspace_right():
    instance.command_socket.send_command("dispatch", args=["workspace", "+1"])
