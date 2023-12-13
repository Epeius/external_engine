# -*- coding: utf-8 -*-
import hashlib
def gen_hash(string):
    return hashlib.md5(string.encode()).hexdigest()
