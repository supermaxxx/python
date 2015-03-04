#!/usr/bin/env python
"""It is usually used for making passwords."""
import random
choice = '123456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ@#$%&'
for i in range(0,21):
    print ''.join(random.sample(choice, 8))
