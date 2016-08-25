from cffi import FFI


ffi = FFI()

ffi.cdef("""
typedef int... off_t;
#define PROT_READ ...
#define PROT_WRITE ...
#define PROT_EXEC ...
#define PROT_NONE ...
#define MAP_PRIVATE ...
#define MAP_FIXED ...
#define MAP_SHARED ...

void mmap_init(off_t offset);
uint16_t mmap_peek16(off_t offset);
void mmap_poke16(off_t offset, uint16_t value);
""")

ffi.set_source("ts7250v2._cmmapwrapper", """
#include<sys/mman.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
volatile uint16_t *map = 0;
void mmap_init(off_t offset){
    int fd;
    fd = open("/dev/mem", O_RDWR|O_SYNC);
    map = mmap(0, getpagesize(), PROT_READ|PROT_WRITE, MAP_SHARED, fd, offset);
}
uint16_t  mmap_peek16(off_t offset){
    uint16_t n;
    n = map[offset/2];
    return n;
}
void mmap_poke16(off_t offset, uint16_t value){
    map[offset/2] = value;
}
""")


class MMIO(object):
    """Class MMIO handles memory-mapped I/O functionality"""
    def __init__(self, offset):
        if (type(offset) != int) and (type(offset) != long):
            raise TypeError("Argument offset must be of type `long` or type `int`")
        from _cmmapwrapper import lib
        self.cmmap = lib
        self.cmmap.mmap_init(offset)

    def peek16(self, offset):
        # bounds check on offset being withing the range defined by TS

        # call ffi peek16 method
        return self.cmmap.mmap_peek16(offset)

    def poke16(self, offset, value):
        # bounds check on offset being within the range defined by TS

        # bounds check on limits for value

        # call ffi poke16 method
        self.cmmap.mmap_poke16(offset, value)
