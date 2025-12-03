import time
import os
import sys
from grub import stage_grub

CLR_BLUE = "\033[34m"
CLR_WHITE = "\033[37m" 
CLR_GREEN = "\033[32m"
CLR_RED = "\033[31m"    
CLR_RESET = "\033[0m"  
CLR_INV = "\033[7m"     
CLR_BLINK = "\033[5m"   

def clear_screen():
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

def print_status(message, status="OK", color=CLR_WHITE, delay=0.01):
    sys.stdout.write(f"{color}{message:<60}")
    if status == "OK":
        sys.stdout.write(f"[{CLR_GREEN} OK {color}]")
    elif status == "FAIL":
        sys.stdout.write(f"[{CLR_RED}FAIL{color}]")
    sys.stdout.write(f"{CLR_RESET}\n")
    sys.stdout.flush()
    time.sleep(delay)

def simulate_typing(text, delay=0.01):

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()


def stage_post():
    clear_screen()
    print(f"{CLR_WHITE}******************************************************************")
    print_status(f"Phoenix Technologies, LTD (c) 2025 - BIOS Rev. 5.12", delay=0.3)
    print_status(f"Processor: Intel(R) Core(TM) i9-14900K @ 3.20GHz (24 Cores)", delay=0.2)
    print_status(f"System Memory Test: 65536MB", delay=0.005) # Быстрый счет
    print_status(f"System Memory Test: 65536MB OK", delay=0.5)
    print_status(f"Initialising Integrated Peripherals...", delay=0.1)
    print_status(f"PCH-P Reset initiated...", delay=0.1)
    
    print("\n" + CLR_WHITE)
    print_status("Detecting Hard Drives (AHCI)...")
    print_status("  Port 00: Samsung 990 Pro 2TB (NVMe 1.4)")
    print_status("  Port 01: WDC WD80EAZZ 8TB (SATA)")
    print_status("  Port 02: TSSTcorp CDDVDW SH-224GB (SATA) - No Media Present")
    
    print_status("PCIe Bus Scan and Initialization...", delay=0.1)
    print_status("  Device 00:02.0 (VGA Compatible Controller): NVIDIA RTX 4090", delay=0.05)
    print_status("  Device 00:14.0 (Network Controller): Intel I226-V 2.5G Ethernet", delay=0.05)
    
    print(f"\n{CLR_WHITE}Press [DEL] to enter Setup. Press [F12] for Boot Menu.")
    print(f"Attempting Boot From: NVMe Drive - Samsung 990 Pro...")
    print("******************************************************************\n")
    time.sleep(1.5)

def stage_kernel():
    clear_screen()
    

    simulate_typing(f"{CLR_WHITE}[    0.000000] Linux version 6.8.0-31-generic (buildd@lcy02-amd64-080)", delay=0.001)
    simulate_typing("[    0.000000] Command line: BOOT_IMAGE=/vmlinuz-6.8.0-31-generic root=UUID=b2f4c9a8-e7d6-44b2-a4e9-21a4f00d3d5f ro quiet splash vt.handoff=7", delay=0.001)
    simulate_typing("[    0.543210] x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'", delay=0.001)
    
    time.sleep(0.3)
    
    print_status("[    1.234567] nvme nvme0: pci: 0000:01:00.0: setting latency timer to 64", delay=0.1)
    print_status(f"[    1.501122] EXT4-fs (nvme0n1p3): mounted filesystem with ordered data mode.", delay=0.1)
    print_status(f"[    1.678001] systemd[1]: systemd 255.4-1ubuntu8 running in system mode", delay=0.1)
    print_status(f"[    1.750000] systemd[1]: Set hostname to <desktop-rig-i9>.", delay=0.1)
    
    time.sleep(0.5)

    print_status("Aquired random seed from bootloader...", status="OK", delay=0.1)
    print_status("Starting udev daemon...", status="OK", delay=0.05)
    print_status("Starting Hostname Service...", status="OK", delay=0.05)
    print_status("Starting Network Manager...", status="OK", delay=0.05)
    print_status("Starting System Logging Service...", status="OK", delay=0.05)
    print_status("Starting User Login Management...", status="OK", delay=0.1)
    
    print("\n" + CLR_WHITE)
    print_status("Reached target Multi-User System.", delay=0.5)


def main():
    try:
        stage_post()
        stage_grub()
        stage_kernel()
        
    except KeyboardInterrupt:
        print(f"\n{CLR_RESET}Boot sequence interrupted by user.")
        sys.exit(0)
    finally:
        print(CLR_RESET)

if __name__ == "__main__":
    clear_screen()
    main()