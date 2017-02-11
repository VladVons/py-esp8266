import gc

#------------------------------------------
def MemFree():
    #gc.collect()
    print("Mem free a1", gc.mem_free()) # 28768


MemFree()

