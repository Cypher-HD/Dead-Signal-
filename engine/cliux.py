# engine/cliux.py
from pyfiglet import Figlet
from termcolor import cprint
from time import sleep

def display_banner():
    f = Figlet(font='slant')
    print('\n' * 2)
    cprint(f.renderText('DEAD SIGNAL'), 'red', attrs=['bold'])

    sleep(0.1)
    cprint('[:: SUBSYSTEM OF: THE BLACKOUT ENGINE ::]', 'magenta', attrs=['bold'])
    sleep(0.1)
    cprint('[:: POWERED BY: THE HACKING PROTOCOL ::]', 'cyan', attrs=['bold', 'underline'])
    print('\n')
    sleep(0.1)
    cprint('> Initializing KHORA Core Linkage...', 'yellow')
    sleep(0.2)
    print('\n' + '=' * 80 + '\n')
