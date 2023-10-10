# Automated Testbench Generator for FPGA Processor\
*By Hamish M 32474741*\
For Monash University Unit ECE2072 Assignment
---
## Purpose
This repo contains code for taking .asm files witten with support for the ECE2072 processor and converting them into Altera Modelsim code used to automatically generate tests for the provided instructions. This is designed to reduce the time taken to generate the test benches needed to test the processor
## Supported Instructions
The python script supports the following instructions

| Instruction        | Description                                       | Shorthand Code      | Supported Version |
|--------------------|---------------------------------------------------|---------------------|-------------------|
| disp Rx            | Moves the value in Rx the display register        | Disp = Rx           | 2                 |
| add Rx, Ry         | Stores Rx + Ry in register Rx                     | Rx = Rx + Ry        | 1                 |
| addi Rx, immediate | Stores Rx + immediate in register Rx              | Rx = Rx + immediate | 1                 |
| sub Rx, Ry         | Stores Rx - Ry in register Rx                     | Rx = Rx - Ry        | 1                 |
| mult Rx, Ry        | Stores Rx * Ry in register Rx                     | Rx = Rx * Ry        | 2                 |
| sll Rx             | Stores Rx shifted left by one bit in register Rx  | Rx = Rx << 1        | 2                 |
| srl Rx             | Stores Rx shifted right by one bit in register Rx | Rx = Rx >> 1        | 2                 |
| movi Rx, immediate | Stores an immediate in register Rx                | Rx = immediate      | 1                 |

As this script is designed to support both a reduced instructin set version (version 1) and a full instruction set version (version 2) the version number represents the instructions supported in each mode.\
Comments can be included by prepending the comment with a semi-colon (;). New lines are ignored. All instructions _will_ generate testbench code. There is no way  to prevent testbench code from being generated for a specific instruction.
* Non-supported instructions will generate the line "// UNSUPPORTED INSTRUCTION"
* Unknown or invalid instructions will generate the line "// UNKNOWN INSTRUCTION"
## Usage
The script takes two arguments; the path to the .asm file, and the version for which the test bench will be generated. If the version is ommitted, it will default to 2.\
```TestBenchASM.py <PATH> [VERSION]```\
The script will generate a testbench.txt file containing the testbench code.
