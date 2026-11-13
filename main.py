import os, sys, time, ctypes, msvcrt

symbols = ['|', '/', '—', '\\']
idx = 0
interval = 0.2
paused = False
quit_ = False

h = ctypes.windll.kernel32.GetStdHandle(-11)
m = ctypes.c_uint32()
ctypes.windll.kernel32.GetConsoleMode(h, ctypes.byref(m))
ctypes.windll.kernel32.SetConsoleMode(h, m.value | 0x0004)

def draw():
    x, y = os.get_terminal_size().columns // 2, os.get_terminal_size().lines // 2
    state = 'PAUSED' if paused else 'RUNNING'
    print(f'\033[1;1H Interval: {interval:.2f}s | {state} | Space: pause\start | +/-: speed | q: quit '.ljust(80)[:80], end='')
    print(f'\033[{y};{x}H{symbols[idx]}', end='')
    sys.stdout.flush()

print('\033[?25l\033[2J\033[H', end='')  # скрыть курсор
last = time.time()
try:
    while not quit_:
        if msvcrt.kbhit():
            k = msvcrt.getch()
            if k in (b'\x00', b'\xe0'):
                msvcrt.getch(); continue
            if k in (b'q', b'Q', b'\xe9', b'\xc9', b'\x1b'):
                quit_ = True
            elif k == b' ':
                paused = not paused
                if not paused:
                    last = time.time()
            elif k in (b'+', b'='):
                interval = min(2.0, interval + 0.05)
            elif k in (b'-', b'_'):
                interval = max(0.05, interval - 0.05)

        if not paused and time.time() - last >= interval:
            idx, last = (idx + 1) % 4, time.time()

        draw()
        time.sleep(0.01)
finally:
    print('\033[?25h\033[2J\033[H', end='')
    print("До свидания!")