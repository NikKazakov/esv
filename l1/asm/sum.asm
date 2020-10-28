N equ 10
section .data
    fmt db "1 + ... + %d = %d", 10, 0
section .text
    extern printf
    global _start
_start:
    ; calc sum
    mov eax, N
    mov edx, 0
label1:
    mul eax
    loop label1
    ; call printf
    push eax
    push dword N
    push fmt
    call printf
    add esp, 12
    ; call exit
    mov ebx, 0
    mov eax, 1
    int 0x80
