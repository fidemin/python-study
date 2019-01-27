# -*- coding: utf-8 -*-
import os

with open('./write.bin', 'wb') as f:
    f.write(os.urandom(10))
