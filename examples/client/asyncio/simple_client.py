import asyncio
import signal
import engineio

loop = asyncio.get_event_loop()
eio = engineio.AsyncClient()
exit_event = asyncio.Event()


async def send_hello():
    message = 'Hello from client side!'
    while not exit_event.is_set():
        print('sending: ' + 'Hello from client side!')
        await eio.send(message)
        try:
            await asyncio.wait_for(exit_event.wait(), timeout=5)
        except asyncio.TimeoutError:
            pass
    await eio.disconnect()


@eio.on('connect')
def on_connect():
    print('connected to server')
    eio.start_background_task(send_hello)


@eio.on('message')
def on_message(data):
    print('received: ' + str(data))


def signal_handler(sig, frame):
    exit_event.set()
    print('exiting')


async def start_server():
    await eio.connect('http://localhost:5000')
    await eio.wait()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    loop.run_until_complete(start_server())
