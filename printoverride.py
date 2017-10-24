from __future__ import print_function

oldPrintFunc = print

def print(text, flush=True, **kwargs):
    oldPrintFunc(text, flush=flush, **kwargs)
    return
