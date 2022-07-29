import os
import sys
from argparse import ArgumentParser
from glob import glob
from time import sleep
import shutil
import curses

def install_themes(scr, target, what, uninstall):
    to_copy = what
    action = 'deleting' if uninstall else 'copying'
    last_action = 'deleted' if uninstall else 'copied'
    scr.addstr(1, 0, 'Target folders: "{}"'.format(target), curses.color_pair(0))
    scr.addstr(2, 0, 'Input folders:', curses.color_pair(0))
    for a_dir_count, a_dir in enumerate(to_copy):
        files = glob(os.path.join('themes', a_dir, '*.pyradio-theme'))
        file_count = 0
        for count in range(0, len(files)):
            Y, X = scr.getmaxyx()
            if not uninstall:
                s_file = os.path.basename(files[count])
            to_file = os.path.basename(files[count]).replace('.pyradio-theme', '') + '-' + a_dir + '.pyradio-theme'
            to_file_path = os.path.join(target, to_file)
            if uninstall:
                try:
                    os.remove(to_file_path)
                    file_count += 1
                except:
                    pass
            else:
                try:
                    shutil.copy(files[count], to_file_path)
                    file_count += 1
                except:
                    pass
            scr.addstr(a_dir_count + 3, 0, '  {0}: {1} file {2}/{3}'.format(a_dir, action, file_count, len(files)), curses.color_pair(0))
            scr.clrtoeol()
            if uninstall:
                msg = '    {}'.format(to_file)[:X]
            else:
                msg = '    {0} -> {1}'.format(s_file, to_file)[:X]
            scr.addstr(a_dir_count + 4, 0, msg, curses.color_pair(0))
            try:
                scr.clrtoeol()
            except:
                pass
            scr.refresh()
            sleep(0.01)
        scr.addstr(a_dir_count + 3, 0, '  {0}: files {1}: {2}/{3}'.format(a_dir, last_action, file_count, len(files)), curses.color_pair(0))
        scr.clrtoeol()

    scr.addstr(a_dir_count + 4, 0, 'Press any key to exit curses...')
    scr.clrtoeol()
    scr.refresh()
    scr.getch()

def make_target(uninstall):
    if sys.platform.startswith('win'):
        target = os.path.join(os.getenv('appdata'), 'pyradio', 'themes')
    else:
        target = os.path.join(os.getenv('HOME', '~'), '.config', 'pyradio', 'themes')

    if not os.path.exists(target) and uninstall:
        print('Nothing to uninstall...\n')
        sys.exit(1)

    if not os.path.exists(target):
        os.makedirs(target)
    if not os.path.exists(target):
        print(1, 0, 'Error: Cannot create output folder: "{}"\n\n'.format(target))
        sys.exit(1)
    return target

parser = ArgumentParser(description='Install PyRadio Base16 themes')
parser.add_argument('-a', '--all', action='store_true',
                    help='install all themes')
parser.add_argument('-d', '--default', action='store_true',
                    help='install default themes only')
parser.add_argument('-l', '--default-alt', action='store_true',
                    help='install default alternative themes only')
parser.add_argument('-r', '--variation', action='store_true',
                    help='install variation themes only')
parser.add_argument('-t', '--variation-alt', action='store_true',
                    help='install variation alternative themes only')
parser.add_argument('-u', '--uninstall', action='store_true',
                    help='uninstall themes (to be used with one of the previous options)')
args = parser.parse_args()

directory_path = os.getcwd()
if not os.path.exists('themes'):
    print('Cannot find the "themes" folder...\n')
    sys.exit(1)

if args.all or args.default or \
        args.default_alt or \
        args.variation or \
        args.variation_alt:
    ''' install themes '''

    target = make_target(args.uninstall)

    if args.uninstall:
        print('PyRadio Base16 themes uninstalled!\n')
    else:
        print('PyRadio Base16 themes installed!\n')

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

    if args.uninstall:
        scr.addstr(0, 0, 'Uninstalling PyRadio Base16 themes', curses.color_pair(0))
    else:
        scr.addstr(0, 0, 'Installing PyRadio Base16 themes', curses.color_pair(0))

    if args.all:
        what = ['default', 'default-alt', 'variation', 'variation-alt']
    else:
        what = []
        if args.default:
            if 'default' not in what:
                what.append('default')
        if args.default_alt:
            if 'default-alt' not in what:
                what.append('default-alt')
        if args.variation:
            if 'variation' not in what:
                what.append('variation')
        if args.variation_alt:
            if 'variation-alt' not in what:
                what.append('variation-alt')
    install_themes(scr, target, what, args.uninstall)
    curses.endwin()
else:
    ''' print help '''
    parser.print_help(sys.stdout)


