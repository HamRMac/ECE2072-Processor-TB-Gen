import sys
import warnings

OPCODES = {
    "disp": "000",
    "add":  "001",
    "addi": "010",
    "sub":  "011",
    "mul":  "100",
    "srl":  "101",
    "sll":  "110",
    "movi": "111"
}

OPCODE_SUPPORTEDV = {
    "disp": 2,
    "add":  1,
    "addi": 1,
    "sub":  1,
    "mul":  2,
    "srl":  2,
    "sll":  2,
    "movi": 1
}

REGISTERS = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "R7": "111",
    "bus":"NULL",
    "display":"NULL"
}

def twos_complement(val, bits):
    """Compute the 2's complement of int value val"""
    if val < 0:
        val = (1 << bits) + val
    return format(val, '0' + str(bits) + 'b')

def instruction_to_machine_code(instruction,ln,v):
    parts = instruction.split()
    opcode = OPCODES[parts[0]]
    instruction = ""
    if parts[0] == "disp":
        register = REGISTERS[parts[1]]  # Remove the comma
        instruction =  f"{opcode}{register}000",
    elif parts[0] == "add":
        register1 = REGISTERS[parts[1][:-1]]  # Remove the comma
        register2 = REGISTERS[parts[2]]
        instruction =  f"{opcode}{register1}{register2}",
    elif parts[0] == "addi":
        register = REGISTERS[parts[1][:-1]]  # Remove the comma
        immediate = twos_complement(int(parts[2]), 9)
        instruction =  f"{opcode}{register}000", immediate
    elif parts[0] == "sub":
        register1 = REGISTERS[parts[1][:-1]]  # Remove the comma
        register2 = REGISTERS[parts[2]]
        instruction =  f"{opcode}{register1}{register2}",
    elif parts[0] == "mul":
        register1 = REGISTERS[parts[1][:-1]]  # Remove the comma
        register2 = REGISTERS[parts[2]]
        instruction =  f"{opcode}{register1}{register2}",
    elif parts[0] == "srl":
        register1 = REGISTERS[parts[1]]  # Remove the comma
        instruction =  f"{opcode}{register1}000",
    elif parts[0] == "sll":
        register1 = REGISTERS[parts[1]]  # Remove the comma
        instruction =  f"{opcode}{register1}000",
    elif parts[0] == "movi":
        register = REGISTERS[parts[1][:-1]]  # Remove the comma
        immediate = twos_complement(int(parts[2]), 9)
        instruction =  f"{opcode}{register}000", immediate
    else:
        warnings.warn(f"Unknown Instruction in line {ln}: '{parts[0]}'")
        return "UNKNOWN INSTRUCTION"
    if OPCODE_SUPPORTEDV[parts[0]] > int(v):
        instruction = "UNSUPPORTED INSTRUCTION"
    return instruction

def verify_instruction(instruction):
    parts = instruction.split()
    opcode = parts[0]
    
    checks = []
    
    if opcode == "disp":
        register = parts[1]
        checks.append(f'if(display !== {register}) begin $display("ERROR: \'disp {parts[1]}\' failed. Expected: %h, Received: %h", {register}, display); errors = errors + 1; end')
        checks.append(f'else $display("Check for disp {parts[1]} passed.");')
        
    elif opcode in ["add", "sub", "mul"]:
        dest = parts[1][:-1]  # Remove the comma
        src2 = parts[2]
        if (dest == src2):
            src2 = dest + "_prev"
        if opcode == "add":
            checks.append(f'if({dest} !== {dest}_prev + {src2}) begin $display("ERROR: \'add {dest}, {src2}\' failed. Expected: %h, Received: %h", {dest}_prev + {src2}, {dest}); errors = errors + 1; end')
        elif opcode == "sub":
            checks.append(f'if({dest} !== {dest}_prev - {src2}) begin $display("ERROR: \'sub {dest}, {src2}\' failed. Expected: %h, Received: %h", {dest}_prev - {src2}, {dest}); errors = errors + 1; end')
        else:  # mul
            checks.append(f'if({dest} !== {dest}_prev * {src2}) begin $display("ERROR: \'mul {dest}, {src2}\' failed. Expected: %h, Received: %h", {dest}_prev * {src2}, {dest}); errors = errors + 1; end')
        checks.append(f'else $display("Check for \'{opcode} {parts[1]} {parts[2]}\' passed.");')
        
    elif opcode == "addi":
        dest = parts[1][:-1]  # Remove the comma
        immediate = int(parts[2])
        checks.append(f'if({dest} !== ({dest}_prev + {immediate})) begin $display("ERROR: \'addi {dest}, {immediate}\' failed. Expected: %h, Received: %h", {dest} + {immediate}, {dest}); errors = errors + 1; end')
        checks.append(f'else $display("Check for \'{opcode} {parts[1]} {immediate}\' passed.");')
        
    elif opcode in ["srl", "sll"]:
        # Just print the results for these, as we can't verify without previous state.
        register = parts[1]
        if opcode == "sll":
            checks.append(f'if({register} !== {register}_prev << 1) begin $display("ERROR: \'ssl {register}\' failed. Expected: %h, Received: %h", {register}_prev << 1, {register}); errors = errors + 1; end')
        else:  # srl
            checks.append(f'if({register} !== {register}_prev >> 1) begin $display("ERROR: \'srl {register}\' failed. Expected: %h, Received: %h", {register}_prev >> 1, {register}); errors = errors + 1; end')
        checks.append(f'else $display("Check for \'{opcode} {register}\' passed.");')
        
    elif opcode == "movi":
        dest = parts[1][:-1]  # Remove the comma
        immediate = int(parts[2]) if int(parts[2])>=0 else f"-9'd{abs(int(parts[2]))}"
        checks.append(f'if({dest} !== {immediate}) begin $display("ERROR: \'movi {dest}, {immediate}\' failed. Expected: %h, Received: %h", {immediate}, {dest}); errors = errors + 1; end')
        checks.append(f'else $display("Check for \'movi  {dest}, {immediate}\' passed.");')
    
    else:
        return ''  # Unknown opcode
    
    return '\n'.join(checks)

def generate_testbench(instruction, ln, version):
    codes = instruction_to_machine_code(instruction, ln+1,version)
    tb = []
    if (not (codes == "UNKNOWN INSTRUCTION")) and (not (codes == "UNSUPPORTED INSTRUCTION")):
        tb.append(f"\n// Load instruction {instruction}")
        for code in codes:
            tb.append(f"din = 9'b{code};")
            tb.append("#10;  // Wait for the next instruction cycle")
        tb.append(f"#{(3-len(codes))*10+8}; // Waiting to get to end of tick 4")
        tb.append(verify_instruction(instruction))
        tb.append(f"#2; // Waiting to get to tick 1")
        return '\n'.join(tb)
    else:
        return '\n//UNKNOWN INSTRUCTION' if (codes == "UNKNOWN INSTRUCTION") else '\n//UNSUPPORTED INSTRUCTION'

if __name__ == "__main__":
    filename = sys.argv[1]
    version = int(sys.argv[2]) if (len(sys.argv) == 3) else 2;
    
    with open(filename, 'r') as file:
        instructions = file.readlines()

    testbench_code = [f"""`timescale 1ns/1ns
/*
Monash University ECE2072: Assignment 
This file contains a Verilog test bench to test the correctness of the processor.

Please enter your student ID:
  32474741
  Written by Hamish M
  This file was automagically generated by a custom python script
  that converts ASM code to the required DIN bits and then generates 
  the required tests to verify the instruction behaved accordingly.
  You can view the script at:
    https://github.com/HamRMac/ECE2072-Processor-TB-Gen/
*/
module proc{"_extension" if (version == 2) else ""}_tb;
// TODO: Implement the logic of your testbench here
initial $display("-=- Loaded proc{"_extension" if (version == 2) else ""}_tb.v -=-");
    
reg clock, rst;
reg [8:0] din;
integer errors = 0;

wire [3:0] tick;
wire [15:0] bus, R0, R1, R2, R3, R4, R5, R6, R7{", display" if (version == 2) else ""};
reg [15:0] bus_prev, R0_prev, R1_prev, R2_prev, R3_prev, R4_prev, R5_prev, R6_prev, R7_prev{", display_prev" if (version == 2) else ""};

{"ext" if (version == 2) else "simple"}_proc myProcessor(.clk(clock), .rst(rst), .din(din), .bus(bus), .tick(tick), .R0(R0), .R1(R1), .R2(R2), .R3(R3), .R4(R4), .R5(R5), .R6(R6), .R7(R7){", .display(display)" if (version == 2) else ""});\n\n"""]
    
    testbench_code.append("// Initialize")
    testbench_code.append("initial begin")
    testbench_code.append("clock = 0;")
    testbench_code.append("rst = 1;")
    testbench_code.append("#40;  // Wait 10 time units for reset")
    testbench_code.append("rst = 0;\n")

    for ln, instruction in enumerate(instructions):
        instruction = instruction.strip()  # Remove leading/trailing whitespace
        if not instruction or instruction.startswith(';'):  # Check if the line is empty or a comment
            continue
        testbench_code.append(generate_testbench(instruction, ln,version))
        testbench_code.append("")


    testbench_code.append('$display("EOT: There was %d errors",errors); $stop;  // Stop the simulation')
    testbench_code.append("end\n")

    testbench_code.append("always begin  // Clock generator")
    testbench_code.append("#5 clock = ~clock;")
    testbench_code.append("end\n")
    
    testbench_code.append("always begin  // Old Value Updater")
    testbench_code.append("#39;")
    for reg in REGISTERS:
        if ((version == 1) and (reg != "display")) or (version == 2):
            testbench_code.append(f"{reg}_prev <= {reg};")
    testbench_code.append("#1;")
    testbench_code.append("end\nendmodule")

    with open(f'testbench_v{version}.txt', 'w') as output:
        output.write('\n'.join(testbench_code[:]))

print(f"Testbench code written to testbench_v{version}.txt")
