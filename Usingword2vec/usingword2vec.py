# coding:utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import math
import os
import random
import zipfile
import numpy as np

from six.moves import urllib
from six.moves import xrange
import tensorflow as tf

# Skip-Gram train language model. Download corpus.
url = 'http://mattmahoney.net/dc/'

def mabe_download(filename, expected_bytes):
    if not os.path.exists(filename):
        filename, _ = urllib.request.urlretrieve(url + filename, filename)
    statinfo = os.stat(filename)
    print(statinfo)
    if statinfo.st_size == expected_bytes:
        print("Found and verified", filename)
    else:
        print()
