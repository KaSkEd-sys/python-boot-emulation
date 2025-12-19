import time
import os
import sys
import tty
import termios

CLR_WHITE = "\033[37m"   
CLR_RESET = "\033[0m"  
CLR_INV = "\033[7m"     

def print_center(text, width):
    return text.center(width)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
        # Доп очистка через escape
        print("\033[2J\033[H", end='')

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        
        # Обработка escape (стрелки)
        if ch == '\x1b':  # ESC
            ch = sys.stdin.read(2)
            if ch == '[A':  # Стрелка вверх
                return 'up'
            elif ch == '[B':  # Стрелка вниз
                return 'down'
        elif ch == '\r' or ch == '\n':  # Enter
            return 'enter'
        elif ch == '\x03':  # Ctrl+C
            return 'exit'
            
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def draw_grub_menu(menu, selected_index, width, height):
    clear_screen()
    
    print(print_center(f"{CLR_WHITE}GNU GRUB  version 2.04{CLR_RESET}", width))
    print("  ┌" + "─" * (width - 6) + "┐  ")
    
    inner_height = height - 8
    
    for line_num in range(inner_height):
        if line_num < len(menu):
            menu_index = line_num
            item = menu[menu_index]
            
            if menu_index == selected_index:
                # Выделенный пункт
                content = f"{CLR_INV}*{item}" + " " * (width - 7 - len(item)) + f"{CLR_RESET}"
                print(f"  │{content}│  ")
            else:
                # Обычный пункт
                content = f"{CLR_WHITE} {item}{CLR_RESET}"
                padding = " " * (width - 7 - len(item))
                print(f"  │{content}{padding}│  ")
        else:
            print("  │" + " " * (width - 6) + "│  ")
    
    print("  └" + "─" * (width - 6) + "┘  \n")
    
    print(print_center(f"{CLR_WHITE}Use the ^ and v keys to select which entry is highlighted.   {CLR_RESET}", width))
    print(print_center(f"{CLR_WHITE}Press enter to boot the selected OS, 'e' to edit the commands{CLR_RESET}", width))
    print(print_center(f"{CLR_WHITE}before booting or 'c' for a command-line.                    {CLR_RESET}", width))

def stage_grub():
    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines
    
    menu = [
        "Ubuntu",
        "Advanced options for Ubuntu",
        "Memory test(memtest86+)",
        "UEFI Firmware Settings",
    ]
    
    selected_index = 0
    
    draw_grub_menu(menu, selected_index, width, height)
    
    while True:
        key = get_key()
        
        if key == 'up':
            selected_index = (selected_index - 1) % len(menu)
            draw_grub_menu(menu, selected_index, width, height)
            
        elif key == 'down':
            selected_index = (selected_index + 1) % len(menu)
            draw_grub_menu(menu, selected_index, width, height)
            
        elif key == 'enter':
            clear_screen()
            print(f"{CLR_WHITE}Booting {menu[selected_index]}...{CLR_RESET}")
            time.sleep(0.5)
            print(f"Loading initial ramdisk ...")
            time.sleep(0.5)
            break
            
        elif key == 'exit':
            break

def main():
    try:
        stage_grub()
        
    except KeyboardInterrupt:
        print(f"\n{CLR_RESET}Boot sequence interrupted by user.")
        sys.exit(0)
    finally:
        print(CLR_RESET)

if __name__ == "__main__":
    clear_screen()
    main()