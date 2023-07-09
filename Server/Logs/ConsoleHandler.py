import sys


def clear_line_1(dir):
    sys.stdout.write("\033[2K")  # Clear current line
    if dir == "left":
        sys.stdout.write("\033[1G")  # Move cursor to the beginning of the line
    elif dir == "right":
        sys.stdout.write("\033[999C")  # Move cursor to the end of the line
    sys.stdout.flush()


def clear_line(dir):
    sys.stdout.write("\033[2K")  # Clear current line
    if dir == 0:
        sys.stdout.write("\033[1G")  # Move cursor to the beginning of the line
    else:
        sys.stdout.write("\033[999C")  # Move cursor to the end of the line
    sys.stdout.flush()


def move_cursor(dx, dy):
    if dx > 0:
        sys.stdout.write("\033[%dC" % dx)  # Move cursor right by dx columns
    elif dx < 0:
        sys.stdout.write("\033[%dD" % (-dx))  # Move cursor left by dx columns

    if dy > 0:
        sys.stdout.write("\033[%dB" % dy)  # Move cursor down by dy rows
    elif dy < 0:
        sys.stdout.write("\033[%dA" % (-dy))  # Move cursor up by dy rows

    sys.stdout.flush()



# test
# # print("[+]test")
# while True:
#     msg = input("shell 192.168.0.151~:>")
#     move_cursor(0, -1)
#     clear_line(0)
#     print(msg)
