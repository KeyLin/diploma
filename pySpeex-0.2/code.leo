<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="15" clone_windows="0"/>
<globals body_outline_ratio="0.27620221948212081">
	<global_window_position top="19" left="0" height="654" width="811"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences allow_rich_text="0">
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v a="E"><vh>NewHeadline</vh>
<v t="T1" tnodeList="1"><vh>@file setup.py</vh></v>
<v t="T2" a="E" tnodeList="2,3,4,5,6,7,8,9,10,11,12,13,14,15"><vh>@file speex.pyx</vh>
<v t="T3" a="E"><vh>cdef externs</vh>
<v t="T4"><vh>string.h</vh></v>
<v t="T5"><vh>stdio.h</vh></v>
<v t="T6"><vh>stdlib.h</vh></v>
<v t="T7"><vh>math.h</vh></v>
<v t="T8"><vh>Python.h</vh></v>
<v t="T9"><vh>speex.h</vh></v>
</v>
<v t="T10" a="E"><vh>cdef class new</vh>
<v t="T11"><vh>c attribs</vh></v>
<v t="T12" a="V"><vh>__init__</vh></v>
<v t="T13"><vh>__dealloc__</vh></v>
<v t="T14"><vh>encode</vh></v>
<v t="T15"><vh>decode</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="T1">import sys

from distutils.core import setup, Extension
from Pyrex.Distutils import build_ext

incDirs = ['../libspeex']
libs = []
libDirs = []
runtimeLibDirs = []
cMacros = []
#extraLinkArgs = ['-g', '/usr/lib/libspeex.a'] # static
extraLinkArgs = ['-g', '-lspeex'] # shared

if sys.platform == 'win32':
    libDirs.append('..\\win32\\Release')
    libs = []
    extraLinkArgs = ['..\\win32\\libspeex\\Release\\libspeex.lib']

speexmodule = Extension('speex',
                        ['speex.pyx'],
                        define_macros=cMacros,
                        include_dirs=incDirs,
                        libraries=libs,
                        library_dirs=libDirs,
                        runtime_library_dirs=runtimeLibDirs,
                        extra_compile_args=['-g'],
                        extra_link_args=extraLinkArgs
                        )

setup(name = 'speex',
      version = '1.0',
      description = 'Python interface to the Speex audio codec',
      ext_modules = [speexmodule],
      cmdclass = {'build_ext': build_ext},
      )
</t>
<t tx="T2">@language python
"""
speex.pyx

Python wrapper for Speex speech codec (www.speex.org)
Defines a 'speex' object through which encoding and
decoding of audio data can be performed.
"""

version = "0.2"

try:
    x = True
except:
    True = 1
    False = 0

@others
</t>
<t tx="T3"># basic system and python facilities

@others
</t>
<t tx="T4">cdef extern from "string.h":

    cdef void *memset(void *s, int c, int n)
    cdef void *memcpy(void *dest, void *src, int n)
</t>
<t tx="T5">cdef extern from "stdio.h":
    int printf(char *format,...)

</t>
<t tx="T6">cdef extern from "stdlib.h":
    void *malloc(int size)
    void *realloc(void *ptr, int size)
    void free(void *ptr)

</t>
<t tx="T7">cdef extern from "math.h":
    double fabs(double x)

</t>
<t tx="T8"># Python-specifics

cdef extern from "Python.h":
    object PyString_FromStringAndSize(char *, int)

</t>
<t tx="T9"># Speex-specifics

cdef extern from "speex.h":
    ctypedef struct SpeexBits:
        char *bytes   # "raw" data
        int  nbBits   # Total number of bits stored in the stream
        int  bytePtr  # Position of the byte "cursor"
        int  bitPtr   # Position of the bit "cursor" within the current byte
        int  owner    # Does the struct "own" the "raw" buffer (member "bytes")
        int  overflow # Set to one if we try to read past the valid data
        int  buf_size # Allocated size for buffer

    ctypedef struct SpeexMode:
        void *mode

    cdef enum SPEEX_SYMBOLS:
        SPEEX_SET_QUALITY
        SPEEX_GET_FRAME_SIZE
        SPEEX_SET_ENH
        SPEEX_GET_ENH

    cdef SpeexMode speex_nb_mode

    cdef void speex_bits_init(SpeexBits *bits)
    cdef void speex_bits_read_from(SpeexBits *bits, char *bytes, int len)
    cdef int speex_bits_write(SpeexBits *bits, char *bytes, int max_len)
    cdef void speex_bits_reset(SpeexBits *bits)
    cdef void speex_bits_destroy(SpeexBits *bits)

    cdef void *speex_encoder_init(SpeexMode *mode)
    cdef int speex_encoder_ctl(void *state,
                               int request,
                               void *ptr)

    cdef int speex_encode(void *state, float *inbuf, SpeexBits *bits)

    cdef void speex_encoder_destroy(void *state)

    cdef void *speex_decoder_init(SpeexMode *mode)
    int speex_decoder_ctl(void *state, int request, void *ptr)
    cdef int speex_decode(void *state,
                          SpeexBits *bits,
                          float *out)
    cdef void speex_decoder_destroy(void *state)
</t>
<t tx="T10">cdef class new:

    @others
</t>
<t tx="T11">cdef void *encState
cdef int encQuality
cdef int encFramesPerBlock
cdef float *encBuf
cdef float *encPtr
cdef int encNumFrames
cdef SpeexBits encBits
cdef int raw

# Data for decoding
cdef void *decState
cdef int decQuality
cdef unsigned char *decBuf
cdef unsigned char *decPtr
cdef unsigned short decBlkSize
cdef int decNumBytes
cdef int decPhase
cdef int decEnhanceOn
cdef SpeexBits decBits
cdef public object debug

cdef public object endianness
</t>
<t tx="T12">def __init__(self, quality=8, raw=0, **kw):
    """
    Create a new speex speech stream object

    Arguments:
     - quality - 0 (lowest) to 10 (highest), default 8

     - raw - set to 1 for encoding from and decoding to string, default 0

    Keywords:
     - debug - set to 1 to issue debug messages, default 0

    The created speex stream object has two methods:
     - encode - encode a block of speech audio data

       Arguments:
        - block of audio data, as sequence of frames, where
          each frame is an int

       Returns:
        - raw string containing encoded data, or
          empty string if there is not yet any encoded
          data available

     - decode - decodes a block of speech audio data

       Arguments:
        - block of encoded data, as raw string,

       Returns:
        - block of audio data, as sequence of ints, or
          an empty sequence if there is no decoded data
          available yet

    Notes:
     - Both of these methods use internal buffering, which means that
       you can feed in data piecemeal. This helps a lot when sending and
       receiving data over the net.
    """

    cdef int is_raw
    #cdef SpeexMode speex_nb_mode

    # Set up encoder
    self.encState = speex_encoder_init(&amp;speex_nb_mode)

    self.encQuality = quality
    is_raw = raw
    self.raw = is_raw
    self.debug = int(kw.get('debug', 0))

    speex_encoder_ctl(self.encState, SPEEX_SET_QUALITY, &amp;self.encQuality)

    #printf("speex1: using new pyrex wrapper, quality=%d\n", self.encQuality)

    speex_encoder_ctl(self.encState, SPEEX_GET_FRAME_SIZE, &amp;self.encFramesPerBlock)
    #printf("encoder frame size=%d\n", self.encFramesPerBlock)
    self.encBuf = &lt;float *&gt;malloc(self.encFramesPerBlock * sizeof(float))
    if not self.encBuf:
        raise Exception("Out of memory")
    memset(self.encBuf, 0, self.encFramesPerBlock * sizeof(float))
    self.encNumFrames = 0
    self.encPtr = self.encBuf
    speex_bits_init(&amp;self.encBits)

    #  Set up decoder
    self.decState = speex_decoder_init(&amp;speex_nb_mode)
    self.decEnhanceOn = 1
    speex_decoder_ctl(self.decState, SPEEX_SET_ENH, &amp;self.decEnhanceOn)
    self.decBuf = &lt;unsigned char *&gt;malloc(2) # just big enough for leading length field
    self.decPhase = 0
    if not self.decBuf:
        raise Exception("Out of memory")
    self.decPtr = self.decBuf
    self.decNumBytes = 0
    speex_bits_init(&amp;self.decBits)
</t>
<t tx="T13">def __dealloc__(self):
    # Destroy the encoder state and data
    speex_encoder_destroy(self.encState)
    if self.encBuf:
        free(self.encBuf)

    # Destroy the decoder state
    speex_decoder_destroy(self.decState)
    if self.decBuf:
        free(self.decBuf)

    # Destroy the bit-packing structs
    speex_bits_destroy(&amp;self.encBits)
    speex_bits_destroy(&amp;self.decBits)

</t>
<t tx="T14">def encode(self, input, raw=None):
    """
    Encode some audio data

    Arguments:
     - data - sequence of audio frames to encode, OR string of 16-bit frames

     - raw  - true if data being passed in is a string of 16-bit frames
       defaults to whatever raw arg was passed to constructor

    Returns:
     - raw string with encoded data
    """

    cdef int numInputFrames
    cdef float *framesBuf, *framesPtr
    # cdef float thisframe
    cdef int i
    cdef int totFrames
    # cdef SpeexBits bits;
    cdef int cbitsSiz
    # cdef int cbitsSiz = 2048
    # cdef char cbits[cbitsSiz]
    cdef char cbits[2048]
    cdef int nBlocks
    cdef int nBytes
    cdef char *bufOut
    cdef int bufOutSiz
    cdef int remainder

    cdef char *rawbuf
    cdef short *frameptr

    cbitsSiz = self.encFramesPerBlock * 5 / 4
    bufOut = &lt;char *&gt;malloc(0)
    bufOutSiz = 0

    inputFramesList = []

    #printf("encode: ok1\n")

    # override raw flag if user has passed in a string
    if raw is None:
        raw = self.raw
    if type(input) is type(""):
        raw = 1
 
    # Determine number of frames
    if raw:
        numInputFrames = len(input) / 2 #  hardwired 16-bit frames
    else:
        numInputFrames = len(input)

    #printf("encode: ok2\n")

    # printf("enc - numInputFrames = %d\n", numInputFrames)

    if numInputFrames == 0:
        return ''

    #printf("encode: ok3\n")

    # Encode what we have, block by block
    totFrames = numInputFrames + self.encNumFrames

    #printf("totFrames=%d, input data size=%d\n",
    #       totFrames, totFrames * sizeof(short))

    framesBuf = &lt;float *&gt;malloc(totFrames * sizeof(float))
    framesPtr = framesBuf
    if not framesBuf:
        raise Exception("Out of memory")

    #printf("encode: ok4\n")

    #  Copy in the fragments we have in buffer
    # printf("copying in buf of %d frames\n", self.encNumFrames)
    for i from 0 &lt;= i &lt; self.encNumFrames:
        framesPtr[i] = self.encBuf[i]

    #printf("encode: ok4a = i=%d, self.encNumFrames=%d\n",
    #       i, self.encNumFrames)

    framesPtr = framesPtr + i

    #printf("encode: ok5\n")

    # Extract the rest from input sequence, depending on whether input is str or list
    # printf("copying extra %d frames from input\n", numInputFrames);
    if raw:
        rawbuf = input
        frameptr = &lt;short *&gt;rawbuf
        for i from 0 &lt;= i &lt; numInputFrames:
            #  assume little-endian - sorry, mac hackers
            # frame = rawptr[0] + 256 * rawptr[1]
            # rawptr += 2
            # *framesPtr++ = (float)frame

            framesPtr[i] = frameptr[i]
        framesPtr = framesPtr + i
        frameptr = frameptr + i
        # thisframe = *frameptr++
        # if (i &lt; 10)
        # {
        #   printf("encode: thisframe=%f\n", thisframe)
        # }
        # *framesPtr++ = thisframe

    else:
        for i from 0 &lt;= i &lt; numInputFrames:
            framesPtr[i] = input[i]
        framesPtr = framesPtr + i
        # thisframe = PyInt_AsLong(PyList_GetItem(input, i))
        # if (i &lt; 10)
        # {
        #   printf("encode: thisframe=%f\n", thisframe)
        # }
        # *framesPtr++ = thisframe

    #printf("written %d frames to buf\n", framesPtr - framesBuf)

    #printf("encode: ok6\n")

    #  Encode these frames
    nBlocks = totFrames / self.encFramesPerBlock
    framesPtr = framesBuf
    for i from 0 &lt;= i &lt; nBlocks:
        # printf("seeking to encode a block, nBlocks=%d\n", nBlocks)
        speex_bits_reset(&amp;self.encBits)
        # printf("ok1 - state=0x%lx, buf=0x%lx, bits=0x%lx\n",
        # self.encState, framesBuf, &amp;self.encBits)
        speex_encode(self.encState, framesPtr, &amp;self.encBits)
        # printf("ok2\n")
        nBytes = speex_bits_write(&amp;self.encBits, cbits, cbitsSiz)
        #printf("nBytes=%d\n", nBytes)
        bufOut = &lt;char *&gt;realloc(bufOut, bufOutSiz+nBytes+2)
        # printf("ok4\n")
        #  write out 2 length bytes
        bufOut[bufOutSiz] = nBytes % 256
        bufOut[bufOutSiz+1] = nBytes / 256
        bufOutSiz = bufOutSiz + 2
        memcpy(bufOut+bufOutSiz, cbits, nBytes)
        # printf("ok5\n")
        bufOutSiz = bufOutSiz + nBytes
        # printf("ok6\n")

        framesPtr = framesPtr + self.encFramesPerBlock

    #printf("encode: ok7\n")

    #  stick remainder, if any, into buffer
    self.encNumFrames = totFrames - (nBlocks * self.encFramesPerBlock)
    remainder = self.encNumFrames * sizeof(float)
    memcpy(self.encBuf, framesPtr, remainder)
    # memset(self.encBuf, 0, self.encFramesPerBlock * sizeof(float))
    # printf("encNumFrames=%d\n", self.encNumFrames)
    # printf("remainder=%d\n", remainder)

    #printf("encode: ok8\n")

    #  ditch temp buffer
    free(framesBuf)

    #printf("encode: ok9\n")

    #  pass back encoded buffer as raw string
    #printf("bufOutSize=%d\n", bufOutSiz)
    return PyString_FromStringAndSize(bufOut, bufOutSiz)


</t>
<t tx="T15">def decode(self, input, raw=None):
    """
    Decode an encoded block, return as sequence of frame tuples

    Arguments:
      - encoded - raw string, containing encoded data
      - raw - True if data is to be returned as string of 16-bit frames, defaults to
        whatever raw value was passed to constructor

    Returns:
      - decoded blocks, as sequence of frames, where each frame
        or a string of these 16-bit frames if raw is True
        is an int
    """

    cdef unsigned char *encBuf
    cdef unsigned char *encBufEnd
    cdef unsigned char *encPtr
    cdef int encBufLen
    cdef int numDecFrames #  number of decoded frames
    # cdef int cbitsSiz
    # cdef char cbits[cbitsSiz]
    cdef float *decFloats
    cdef float *decFloats1
    cdef short *decShorts
    cdef short *decShorts1
    cdef int decBlocks
    cdef int i
    cdef int is_raw
    cdef int needed
    cdef int newNumFrames
    cdef char *tmp

    #printf("decode: ok1\n")

    tmp = input
    encBuf = &lt;unsigned char *&gt;tmp
    encBufEnd = NULL
    encPtr = NULL
    encBufLen = 0
    decFloats = &lt;float *&gt;malloc(0)
    decShorts = &lt;short *&gt;malloc(0)
    decBlocks = 0

    if raw is None:
        raw = self.raw
    is_raw = raw

    #printf("decode: ok2, raw=%d\n", is_raw)

    #  We get an earlymark if caller provided no data
    encBufLen = len(input)
    if encBufLen == 0:
        if is_raw:
            return ''
        else:
            return []

    #printf("decode: ok3\n")

    #  decode the sucker
    encPtr = encBuf
    encBufEnd = encBuf + encBufLen

    #printf("decode: ok4, len=%d\n", encBufLen)

    while encPtr &lt; encBufEnd:
        #  state depends on whether we've received the block header count bytes
        if self.decPhase == 0:
            #  Grab LSB of block size
            self.decBuf[0] = encPtr[0]
            #printf("decode: ok4a - LSB=%02x\n", encPtr[0])
            self.decPhase = 1
            encPtr = encPtr + 1
            encBufLen = encBufLen - 1
            continue
        elif self.decPhase == 1:
            #  Grab MSB of block size and determine total block size
            self.decBuf[1] = encPtr[0]
            #printf("decode: ok4b - LSB=%02x\n", encPtr[0])
            self.decBlkSize = self.decBuf[0] + 256 * self.decBuf[1]
  
            #  resize dec buffer to suit
            #  todo - find better way to sanity check the size
            self.decBuf = &lt;unsigned char *&gt;realloc(
                &lt;void *&gt;self.decBuf,
                self.decBlkSize)
            self.decPtr = self.decBuf
            self.decNumBytes = 0
            self.decPhase = 2
            encPtr = encPtr + 1
            encBufLen = encBufLen - 1
            continue
        else:
            #printf("decode: ok4c siz=%d decnumbytes=%d\n",
            #       self.decBlkSize, self.decNumBytes)
            needed = self.decBlkSize - self.decNumBytes
  
            #printf("decode: ok4d encBufLen=%d needed=%d\n",
            #       encBufLen, needed)
            #  do we have enough input data to complete a frame?
            if encBufLen &gt;= needed:
                newNumFrames = (decBlocks + 1) * self.encFramesPerBlock
  
                #  great - decode frame and add to our array of shorts
                memcpy(self.decPtr,
                       encPtr,
                       self.decBlkSize - self.decNumBytes)
                encPtr = encPtr + needed
                encBufLen = encBufLen - needed
  
                #  do the decoding
                #  expand shorts and floats buffers
                decShorts = &lt;short *&gt;realloc(decShorts, newNumFrames * sizeof(short))
                decShorts1 = decShorts + decBlocks * self.encFramesPerBlock
                decFloats = &lt;float *&gt;realloc(decFloats, newNumFrames * sizeof(float))
                decFloats1 = decFloats + decBlocks * self.encFramesPerBlock
  
                # Copy the data into the bit-stream struct
                speex_bits_read_from(&amp;self.decBits, &lt;char *&gt;self.decPtr, self.decBlkSize)
  
                # Decode the data
                speex_decode(self.decState, &amp;self.decBits, decFloats1)
  
                # Copy from float to short (16 bits) for output
                for i from 0 &lt;= i &lt; self.encFramesPerBlock:
                  decShorts1[i] = decFloats1[i]
  
                self.decPhase = 0 #  back to awaiting LSB of count header
                self.decNumBytes = 0
                if self.debug:
                    printf("self.decBuf=%lx\n", self.decBuf)
                self.decBuf = &lt;unsigned char *&gt;realloc(self.decBuf, 2)
                decBlocks = decBlocks + 1
                continue
            else:
                #printf("decode: ok4e\n")

                #  not enough to decode another speex frame - just stick into buffer
                if self.debug:
                    printf("decPtr=%lx, encPtr=%lx, encBufLen=%d\n",
                            self.decPtr, encPtr, encBufLen)
                memcpy(self.decPtr, encPtr, encBufLen)
                self.decPtr = self.decPtr + encBufLen
                encBufLen = 0
                break

    #printf("decode: ok5\n")

    #  did we get anything?
    if decBlocks &gt; 0:
        numDecFrames = decBlocks * self.encFramesPerBlock
       
        if is_raw:
            ret = PyString_FromStringAndSize(&lt;char *&gt;decShorts, numDecFrames * 2)
        else:
            #  build up a sequence of tuples
            ret = []
            for i in range(numDecFrames):
                ret.append(decShorts[i])
    else:
        if is_raw:
            ret = ""
        else:
            ret = []

    #printf("decode: ok6\n")

    free(decShorts)
    free(decFloats)
    return ret

    # return Py_BuildValue("s#", decBuf, decBufLen)


</t>
</tnodes>
</leo_file>
