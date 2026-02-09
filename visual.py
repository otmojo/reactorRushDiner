import os
import time
import sys

class YangiConsole:
    # ANSI color codes
    GREEN = "\033[0;32m"
    BRIGHT_GREEN = "\033[1;32m"
    RED = "\033[0;31m"
    CYAN = "\033[0;36m"
    YELLOW = "\033[1;33m"
    RESET = "\033[0m"

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def banner():
        YangiConsole.clear()
        art = f"""{YangiConsole.BRIGHT_GREEN}
██████╗ ███████╗ █████╗  ██████╗████████╗ ██████╗ ██████╗ 
██╔══██╗██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██████╔╝█████╗  ███████║██║        ██║   ██║   ██║██████╔╝
██╔══██╗██╔══╝  ██╔══██║██║        ██║   ██║   ██║██╔══██╗
██║  ██║███████╗██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
        >>> RUSH DINER SIMULATION PROTOCOL <<<
{YangiConsole.RESET}"""
        print(art)
        print(f"{YangiConsole.GREEN}[SYSTEM] CORE MODULES INITIALIZED.{YangiConsole.RESET}")

    @staticmethod
    def log(message, level="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        levels = {
            "INFO": YangiConsole.GREEN,
            "WARN": YangiConsole.YELLOW,
            "ERROR": YangiConsole.RED,
            "SUCCESS": YangiConsole.BRIGHT_GREEN
        }
        color = levels.get(level, YangiConsole.CYAN)
        print(f"{color}[{timestamp}] [{level}] >> {message}{YangiConsole.RESET}")

    @staticmethod
    def table(headers, rows):
        print(f"\n{YangiConsole.CYAN}" + "="*60)
        widths = [20, 20, 20]
        header_str = "".join(f"{h:<{w}}" for h, w in zip(headers, widths))
        print(f"| {header_str}")
        print("-" * 60)
        for row in rows:
            row_str = "".join(f"{str(cell):<{w}}" for cell, w in zip(row, widths))
            print(f"| {YangiConsole.GREEN}{row_str}{YangiConsole.RESET}")
        print(f"{YangiConsole.CYAN}" + "="*60 + f"{YangiConsole.RESET}\n")

    @staticmethod
    def progress_bar(current, total, label="PROCESSING"):
        percent = 100 * (current / float(total))
        bar_length = 30
        filled = int(bar_length * current // total)
        bar = '█' * filled + '-' * (bar_length - filled)
        # \r carriage return to overwrite the line
        sys.stdout.write(f'\r{YangiConsole.GREEN}[{label}] |{bar}| {percent:.1f}%{YangiConsole.RESET}')
        sys.stdout.flush()
        if current == total: print()

    @staticmethod
    def input_prompt(prompt_text):
        print(f"\n{YangiConsole.BRIGHT_GREEN}>> {prompt_text}{YangiConsole.RESET}", end=" ")
        return input().strip()