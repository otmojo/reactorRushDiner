import sys
import asyncio
import time
import os
from server_event import run_event_server
from server_thread import run_thread_server
from sim_restaurant import run_multi_thread_sim, run_nio_sim
from visual import YangiConsole

def run_simulation():
    YangiConsole.log("INITIALIZING SIMULATION ENGINE...", "INFO")
    num_customers = 5000
    
    YangiConsole.log(f"CONFIGURATION: {num_customers} REQUESTS", "INFO")
    
    YangiConsole.log("STARTING THREAD POOL SIMULATION...", "INFO")
    mt_t, mt_cpu = run_multi_thread_sim(num_customers=num_customers, num_workers=10)
    
    YangiConsole.log("STARTING ASYNC EVENT LOOP SIMULATION...", "INFO")
    ev_t, ev_cpu = asyncio.run(run_nio_sim(num_customers=num_customers))
    
    headers = ["MODE", "THROUGHPUT (req/s)", "VIRTUAL CPU LOAD (%)"]
    rows = [
        ["THREAD_POOL", f"{mt_t:.2f}", f"{mt_cpu:.1f}"],
        ["ASYNC_CORE", f"{ev_t:.2f}", f"{ev_cpu:.1f}"]
    ]
    YangiConsole.table(headers, rows)
    YangiConsole.log("SIMULATION COMPLETE.", "SUCCESS")

def main_menu():
    while True:
        YangiConsole.banner()
        print(f"{YangiConsole.GREEN}SELECT OPERATION MODE:{YangiConsole.RESET}")
        print(f"[{YangiConsole.BRIGHT_GREEN}1{YangiConsole.RESET}] RUN PERFORMANCE SIMULATION")
        print(f"[{YangiConsole.BRIGHT_GREEN}2{YangiConsole.RESET}] START ASYNC SERVER (8888)")
        print(f"[{YangiConsole.BRIGHT_GREEN}3{YangiConsole.RESET}] START THREAD SERVER (8889)")
        print(f"[{YangiConsole.RED}0{YangiConsole.RESET}] EXIT")
        
        choice = YangiConsole.input_prompt("ENTER COMMAND:")
        if choice == "1":
            run_simulation()
            input("\nPRESS ENTER TO CONTINUE...")
        elif choice == "0":
            break

if __name__ == "__main__":
    if os.name == 'nt': os.system('') #  Windows ANSI support
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "sim":
            run_simulation()
        else:
            main_menu()
    except KeyboardInterrupt:
        sys.exit(0)