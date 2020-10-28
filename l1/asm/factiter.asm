N equ 3
section .data
    fmt db "%d! = %d", 10, 0
section .text
    extern printf
    global _start
fact:
    cmp ecx, 0
    je fact2
fact1:
    mul ecx
    loop fact1
fact2:
    ret
_start:
    ; init values
    mov ecx, N
    mov eax, 1
    ; main
    call fact
    ; print
    push eax
    push N
    push fmt
    call printf
    ; exit
    mov ebx, 0
    mov eax, 1
    int 0x80
