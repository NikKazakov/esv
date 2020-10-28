N equ 3
section .data
    fmt db "%d! = %d",10,0
section .text
    extern printf
    global _start
fact:
    cmp ebx, 0
    je fact1
    mul ebx
    dec ebx
    call fact
fact1:
    ret
_start:
    ; init numbers
    mov ebx, N
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
