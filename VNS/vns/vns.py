#!/usr/bin/python

import sys

import myGUI

# =========================================================

def main():

    network_controler = myGUI.MyGUI()
    network_controler.run()

    sys.exit()

# ===========================================================
if __name__ == '__main__':
    main()