# Source locations

All paths below are relative to the separately obtained FEILIAN submission root.
The third-party sources and PDF are not included. The [input manifest](input_manifest.json)
records all 74 file hashes. Line numbers refer to those exact bytes, not to a later revision.
The PDF has 68 pages; its viewer page number is one greater than its printed page number.

<a id="source-1"></a>

## Specification.pdf

File: `Algorithm specifications/Specification.pdf`

SHA-256: `8e3a9a109f3188ab57cbd0156c243f80a6453051cf98006dfef11d66bdeb5fa8`

<a id="source-2"></a>

## 8SC core

File: `Implementations/Additional_Implementation/FEILIAN_8SC/core.sv`

Source line cited: 136. Read the enclosing function/state machine for context.

SHA-256: `42509a8276c876a50eba131a4cbe7ea07aadcc6c2ae0ec0c7c1793790c13b218`

<a id="source-3"></a>

## compression.sv

File: `Implementations/Additional_Implementation/FEILIAN_8SC/compression.sv`

Source line cited: 76. Read the enclosing function/state machine for context.

SHA-256: `eb1c0680be1eabfdf49336fc7b206be738f60029955b71f51025952b2721640d`

<a id="source-4"></a>

## 1SC core

File: `Implementations/Additional_Implementation/FEILIAN_1SC/core.sv`

Source line cited: 134. Read the enclosing function/state machine for context.

SHA-256: `4f48f341c0c0c44954344fa979c885f53422e66303247535936bf983311e16fd`

<a id="source-5"></a>

## 4SC core

File: `Implementations/Additional_Implementation/FEILIAN_4SC/core.sv`

Source line cited: 134. Read the enclosing function/state machine for context.

SHA-256: `4f48f341c0c0c44954344fa979c885f53422e66303247535936bf983311e16fd`

<a id="source-6"></a>

## 2SC core

File: `Implementations/Additional_Implementation/FEILIAN_2SC/core.sv`

Source line cited: 120. Read the enclosing function/state machine for context.

SHA-256: `3dfd52e0c5765ae457106e94387e6a50da3dd7cc630d16d7cea32a61b81e8091`

<a id="source-7"></a>

## round functions

File: `Implementations/Reference_Implementation/FEILIAN1024/CryptHash_AlgorithmInstance.c`

Source line cited: 219. Read the enclosing function/state machine for context.

SHA-256: `421ee5370e0c5ed33618f371b4ea5a3b14a55f7bc71f0237bf40274e4229f02e`

<a id="source-8"></a>

## counter helper

File: `Implementations/Reference_Implementation/FEILIAN1024/CryptHash_AlgorithmInstance.c`

Source line cited: 132. Read the enclosing function/state machine for context.

SHA-256: `421ee5370e0c5ed33618f371b4ea5a3b14a55f7bc71f0237bf40274e4229f02e`

<a id="source-9"></a>

## padding function

File: `Implementations/Reference_Implementation/FEILIAN1024/CryptHash_AlgorithmInstance.c`

Source line cited: 74. Read the enclosing function/state machine for context.

SHA-256: `421ee5370e0c5ed33618f371b4ea5a3b14a55f7bc71f0237bf40274e4229f02e`

<a id="source-10"></a>

## drng.c

File: `Implementations/Reference_Implementation/FEILIAN1024/drng.c`

Source lines: 31 and 303 (partial-byte mask), 36 and 90–94 (rotations), 200–262 (derivation/initialization), 317–319 (public initialization wrapper). Read the enclosing functions and callers. The file is identical in all six FEILIAN directories; see [shared_drng.json](shared_drng.json).

SHA-256: `0df0ac78c828bd43bf05724398fa530767d753aa7801a1d1fa5d621321ec797e`

<a id="source-11"></a>

## public API

File: `Implementations/Reference_Implementation/FEILIAN1024/CryptHash_AlgorithmInstance.c`

Source line cited: 353. Read the enclosing function/state machine for context.

SHA-256: `421ee5370e0c5ed33618f371b4ea5a3b14a55f7bc71f0237bf40274e4229f02e`

<a id="source-12"></a>

## SIMD implementation

File: `Implementations/Optimized_Implementation/FEILIAN_SIMD1024/CryptHash_AlgorithmInstance.c`

Source line cited: 360. Read the enclosing function/state machine for context.

SHA-256: `39c53e5177558d8b2f4432a05b1ffc21e9220152420cf0f8c6a187ad64e3e765`


<a id="source-13"></a>

## Hardware top-level parameters and byte-count interface

File: `Implementations/Additional_Implementation/FEILIAN_1SC/feilian.sv`

Source lines: 8, 40, 62 and 123; the same unparameterized core instantiation occurs in all four architectures. Read the enclosing interface and call chain.

SHA-256: `088e6728e18a00f70f50f0237bdbaccb665e0b794041d8dbb5861e705d254785`

<a id="source-14"></a>

## Shared KAT initialization calls

File: `Implementations/Reference_Implementation/FEILIAN1024/KAT_CryptHash.c`

Source lines: 296, 379, 487 and 601. Read the enclosing interface and call chain.

SHA-256: `ab4d08d943b3cfaff3e9418964753f99b28226f84dfc70427fc677baec868268`

<a id="source-15"></a>

## Submission test-infrastructure requirements

File: `Implementations/README.txt`

Source lines: 46–63. Read the enclosing interface and call chain.

SHA-256: `c8b8eb237a1ab3da06338262a159852194ffd4cf1e4f5267adcb89fe7e6d0bc5`
