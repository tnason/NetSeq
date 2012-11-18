"""System operations"""

import os.path
import sys

def get_atlas():
    """Find the location of the image atlas"""

    """Figure out whether we are in a binary or source"""
    if getattr(sys, 'frozen', None):
        atlas_location = 'atlas://' + os.path.join(sys._MEIPASS, 'netseq-theme')
    else:
        script_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        image_dir = os.path.join(script_dir, "images")
        atlas_location = "atlas://" + os.path.join(image_dir, "netseq-theme")

    return atlas_location

def get_item_in_atlas(item):
    """Get a string

    Arguments:
    item: String name of item in atlas

    Return:
    'atlas' path to item

    """

    return os.path.join(get_atlas(), item)

def get_kv_dir():
    """Find the directory of the .kv style file"""
    
    if getattr(sys, 'frozen', None):
        kv_dir = sys._MEIPASS
    else:
        kv_dir = os.path.dirname(os.path.realpath(__file__))

    return kv_dir

def get_kv_file():
    """Get the name of the kv file"""
    
    KV_FILENAME = 'netseq.kv'
    return os.path.join(get_kv_dir(), KV_FILENAME)

def get_images_dir():
    """Find the image directory"""

    if getattr(sys, 'frozen', None):
        images_dir = sys._MEIPASS
    else:
        images_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

    return images_dir

def get_sounds_dir():
    """Find the image directory"""

    if getattr(sys, 'frozen', None):
        sounds_dir = sys._MEIPASS
    else:
        sounds_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "sounds")

    return sounds_dir
