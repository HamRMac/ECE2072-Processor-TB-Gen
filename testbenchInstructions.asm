; Systematic Tests
; Test 'movi' opcode
movi R0, 5
movi R1, 7

; Test 'addi' opcode
addi R2, 3
addi R3, 2

; Test 'disp' opcode
disp R0
disp R3

; Test 'add' opcode
add R0, R0
add R1, R2

; Test 'sub' opcode
sub R0, R1
sub R7, R2

disp R0
disp R7

; Combined Instruction Tests Block 1

; Obscure combination: Multiple additions and a subtraction 
movi R1, -10
movi R2, 10
movi R3, 20
add R2, R1
add R3, R2
sub R3, R1
disp R3

; Combined Instruction Tests Block 2

; Test of chaining results: Result of one operation becomes operand for the next
movi R1, 15
addi R2, 3
add R3, R1
add R4, R2
mul R3, R4
disp R4

; Combined Instruction Tests Block 3

; Test 'movi' followed by a sequence of operations
movi R2, 25
movi R3, 0
movi R4, 1
addi R3, 5
add R3, R2
sub R3, R4
srl R3
disp R3

; Edge Cases

movi R1, -256
movi R6, 0
movi R7, 255
movi R0, 0
add R0, R7
disp R0
movi R6, -1
add R1, R6
disp R1
