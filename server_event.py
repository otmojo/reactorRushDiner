import asyncio
from visual import YangiConsole

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    try:
        data = await asyncio.wait_for(reader.read(1024), timeout=6.0)
        if not data:
            return
        YangiConsole.log(f"RECV {addr}: {data.decode().rstrip()}", "INFO")
        await asyncio.sleep(0.08)           # Simulating processing time
        writer.write(data)
        await writer.drain()
    except asyncio.TimeoutError:
        YangiConsole.log(f"{addr} TIMEOUT -> BACKPRESSURE APPLIED", "WARN")
    except Exception as e:
        YangiConsole.log(f"ERROR {addr}: {e}", "ERROR")
    finally:
        writer.close()
        await writer.wait_closed()

async def run_event_server():
    host = '127.0.0.1'
    port = 8888
    server = await asyncio.start_server(
        handle_client, host, port, limit=80
    )
    YangiConsole.log(f"EVENT-DRIVEN SERVER LISTENING ON {host}:{port} (MAX CONCURRENCY≈80)", "SUCCESS")
    async with server:
        await server.serve_forever()
