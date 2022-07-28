import os
import sys
from time import sleep
import shutil
import curses
import threading
from glob import glob
from argparse import ArgumentParser
try:
    import queue
except:
    import Queue as queue

win = None

def print_msg(msg):
    win.move(0, 0)
    win.insdelln(1)
    win.addstr(msg, curses.color_pair(0))
    win.refresh()

def make_target():
    if sys.platform.startswith('win'):
        target = os.path.join(os.getenv('appdata'), 'pyradio', 'themes')
    else:
        target = os.path.join(os.getenv('HOME', '~'), '.config', 'pyradio', 'themes')

    if not os.path.exists(target):
        os.makedirs(target)
    if not os.path.exists(target):
        print(1, 0, 'Error: Cannot create output folder: "{}"\n\n'.format(target))
        sys.exit(1)
    target = os.path.join(target, 'cycle_base16_themes.pyradio-theme')
    ''' reset the file '''
    try:
        with open(target, 'w') as f:
            pass
    except:
        print(1, 0, 'Error: Cannot create output file: "{}"\n\n'.format(target))
        sys.exit(1)
    return target

def copy_a_theme(scr, in_file, out_file, a_dir):
    o_file = os.path.join(os.path.dirname(out_file), os.path.basename(in_file).replace('.pyradio-theme', '-' + a_dir + '.pyradio-theme'))
    try:
        shutil.copy(in_file, o_file)
        print_msg('Theme copyied: {}'.format(os.path.basename(o_file)).replace('.pyradio-theme', ''))
    except:
        print_msg('Theme copy failed: {}'.format(os.path.basename(o_file)).replace('.pyradio-theme', ''))

def copy_theme_group(scr, in_file, out_file, dirs):
    theme_name = os.path.basename(in_file).replace('.pyradio-theme', '')
    for n in dirs:
        theme_name = theme_name.replace(n, '')
    # print_msg('theme_name: {}'.format(theme_name))

    in_list = []
    out_list = []
    error = False
    for n in dirs:
        in_list.append(os.path.join('themes', n, theme_name + '.pyradio-theme'))
        out_list.append(os.path.join(os.path.dirname(out_file), theme_name + '-' + n + '.pyradio-theme'))
        # print_msg('in: ' + in_list[-1])
        # print_msg('out: ' + out_list[-1])
        try:
            shutil.copy(in_list[-1], out_list[-1])
        except:
            error = True
    if error:
        print_msg('Theme group copy failed: ' + theme_name)
    else:
        print_msg('Theme group copyied: ' + theme_name)


def do_copy_files(scr, out_file, stop, delay, th_start_count, que):
    ''' thread to copy files to out file '''
    start_count = int(th_start_count / 4)
    scr.clrtoeol()
    dirs = (
        'default',
        'default-alt',
        'variation',
        'variation-alt'
    )
    files = glob(os.path.join('themes', 'default', '*.pyradio-theme'))
    files.sort()
    y, x = scr.getmaxyx()
    msg = ' Available commands:'
    scr.addstr(8, 0, msg.ljust(x), curses.A_REVERSE)
    msg = ' Total number of themes: {0}, delay: {1} sec'.format(4 * len(files), delay())
    scr.addstr(1, 0, msg.ljust(x), curses.A_REVERSE)
    scr.addstr(0, 0, ' Cycle PyRadio Base16 Themes', curses.A_BOLD)

    end_count = len(files)
    scr.clrtoeol()
    while True:
        max_len = len(str(len(files)))
        for i in range(start_count, end_count):
            for n in range(0, 4):
                num = str(4 * i + n + 1)

                scr.addstr(n+3, 0, '   ' + num.rjust(max_len)  + '. ' + os.path.basename(files[i]).replace('.pyradio-theme', '') + '-' + dirs[n], curses.color_pair(0))
                scr.clrtoeol()
                if stop():
                    return
            scr.refresh()
            ''' delete all ticks '''
            for n in range(0, 4):
                scr.addstr(n + 3, 1, ' ', curses.color_pair(0))
            for n in range(0, 4):
                # scr.addstr(n + 3, 1, '>', curses.color_pair(0))
                scr.addstr(n + 3, 1, '>', curses.A_BOLD)
                if n > 0:
                    scr.addstr(n + 2, 1, ' ', curses.color_pair(0))
                ''' copy file '''
                in_file = os.path.join('themes', dirs[n], os.path.basename(files[i]))
                shutil.copy(in_file, out_file)

                y, x = scr.getmaxyx()
                msg = ' Available commands:'
                scr.addstr(8, 0, msg.ljust(x), curses.A_REVERSE)
                msg = ' Total number of themes: {0}, delay: {1} sec'.format(4 * len(files), delay())
                scr.addstr(0, 0, ' Cycle PyRadio Base16 Themes', curses.A_BOLD)
                scr.addstr(1, 0, msg.ljust(x), curses.A_REVERSE)

                msg = '''   + / .    Increase delay
   - / ,    Decrease delay
   c , C    Copy theme by name / group
   q        Exit
'''
                scr.addstr(9, 0, msg, curses.color_pair(0))

                for l in range(9, 13):
                    for k in 3, 7:
                        scr.chgat(l, k, 1, curses.A_BOLD)

                msg = ' Messages:'
                scr.addstr(14, 0, msg.ljust(x), curses.A_REVERSE)

                scr.refresh()
                step = int(delay() / .2) + 1
                for _ in range(0, step):
                    sleep(.2)
                    try:
                        command = que.get(block=False)
                    except queue.Empty:
                        command = None
                    if command is not None:
                        if command == ord('c'):
                            copy_a_theme(scr, in_file, out_file, dirs[n])
                        elif command == ord('C'):
                            copy_theme_group(scr, in_file, out_file, dirs)
                    if stop():
                        return
                if stop():
                    return
        start_count = 0
        if stop():
            return



parser = ArgumentParser(description='Cycle through PyRadio Base16 themes')
parser.add_argument('-s', '--start',
                    help='start with theme number')
parser.add_argument('-d', '--delay',
                    help='counter delay')
args = parser.parse_args()

''' start curses '''
scr = curses.initscr()
curses.start_color()
curses.use_default_colors()
try:
    curses.curs_set(0)
except:
    pass
scr.nodelay(0)
curses.noecho()
curses.cbreak()

start_count = 0
if args.start:
    try:
        start_count = int(args.start) - (int(args.start) % 4)
    except:
        pass
delay = 2
if args.delay:
    try:
        delay = float(args.delay)
    except:
        pass

out_file = make_target()

msg =  '''Please execute PyRadio now and "watch" the "cycle_base16_themes" theme

To do that:
  1. Execute PyRadio
  2. Press "t" to open the "Themes Selection" window
  3. Select the "cycle_base16_themes" entry
  4. Press "c" to watch it
  5. Press "ESCAPE" to close the "Themes Selection" window

When you are ready, please press any key to continue...


Parameters:
  Start counter: {0}
  Counter delay: {1} sec
'''

scr.addstr(0, 0, msg.format(start_count, delay), curses.color_pair(0))
scr.refresh()
scr.getch()
scr.clear()
scr.refresh()

y, x = scr.getmaxyx()
win = curses.newwin(y-15, x, 15, 0)
print_msg('Program started...')
que = queue.Queue()

stop_thread = False
copy_thread = threading.Thread(
    target=do_copy_files,
    args=(
        scr,
        out_file,
        lambda: stop_thread,
        lambda: delay,
        start_count,
        que
    )
)
copy_thread.start()

while True:
    char = scr.getch()
    if char == curses.KEY_RESIZE:
        ny, nx = scr.getmaxyx()
        win.resize(ny-15, nx)
        win.mvwin(15, 0)
        # win.touchwin()
        # win.redrawwin()
        # win.refresh()
    elif char == ord('q'):
        stop_thread = True
        break
    elif char in (ord('+'), ord('.')):
        delay = round(delay + .1, 1)
        print_msg('Delay increased by .1 sec...')
    elif char in (ord('-'), ord(',')):
        if delay > .5:
            delay = round(delay - .1, 1)
            print_msg('Delay decreased by .1 sec...')
    elif char in (ord('c'), ord('C')):
        try:
            que.put(char, block=False)
        except queue.Full:
            pass


print_msg('Waiting for threads to terminate...')
copy_thread.join()
curses.endwin()
os.remove(out_file)
