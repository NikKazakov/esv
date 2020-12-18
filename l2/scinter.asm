section .data
    arg0 db "/usr/bin/python", 0
section .text
    global _start
_start:
    xor eax, eax
    push eax
    push 0x6e6f6874  ;noht
    push 0x79702f2f  ;yp//
    push 0x6e69622f  ;nib/
    push 0x7273752f  ;rsu/
    mov ebx, esp
    mov ecx, eax
    mov edx, eax
    mov al, 0xb
    int 0x80
    xor eax, eax
    inc eax
    int 0x80
