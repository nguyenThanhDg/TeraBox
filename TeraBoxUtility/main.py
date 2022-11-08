import sys
import common.constant as Constant
from util.log import log_error, setup_logging
from util.tera import TeraBox

setup_logging()


def greet():
    str = ("████████╗███████╗██████╗░░█████╗░██████╗░░█████╗░██╗░░██╗██╗░░░██╗████████╗██╗██╗░░░░░██╗████████╗██╗░░░██╗\n"
    "╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗██╔╝██║░░░██║╚══██╔══╝██║██║░░░░░██║╚══██╔══╝╚██╗░██╔╝\n"
    "░░░██║░░░█████╗░░██████╔╝███████║██████╦╝██║░░██║░╚███╔╝░██║░░░██║░░░██║░░░██║██║░░░░░██║░░░██║░░░░╚████╔╝░\n"
    "░░░██║░░░██╔══╝░░██╔══██╗██╔══██║██╔══██╗██║░░██║░██╔██╗░██║░░░██║░░░██║░░░██║██║░░░░░██║░░░██║░░░░░╚██╔╝░░\n"
    "░░░██║░░░███████╗██║░░██║██║░░██║██████╦╝╚█████╔╝██╔╝╚██╗╚██████╔╝░░░██║░░░██║███████╗██║░░░██║░░░░░░██║░░░\n"
    "░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░░╚════╝░╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░╚═╝╚══════╝╚═╝░░░╚═╝░░░░░░╚═╝░░░\n")
    print(str)


if __name__ == '__main__':
    greet()
    Constant.init()
    try:
        a = ['nguyenthanhdungktum@gmail.com', 'terabox269@gmail.com']
        tera = TeraBox(a)
        # tera.upload()
        tera.download()

    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        log_error(e, is_critical=True)
