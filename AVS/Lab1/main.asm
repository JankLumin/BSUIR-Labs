[BITS 16]
[ORG 0x7C00]

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    mov si, msg_real_mode
    call print_string_real_mode

    call wait_for_keypress

    lgdt [gdt_descriptor]
    mov eax, cr0
    or eax, 1
    mov cr0, eax
    jmp CODE_SEL:protected_mode_entry

[BITS 32]
protected_mode_entry:
    mov ax, DATA_SEL
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    mov esp, 0x7C00

    mov edi, 0xB8000
    mov ax, 0x0720
    mov ecx, 80*25
    rep stosw

    mov edi, 0xB8000
    mov esi, msg_protected_mode
    call print_string

    mov ecx, 2000000000 
    delay_loop:
        loop delay_loop

    jmp 0xF000:0xFFF0

[BITS 16]

print_string_real_mode:
    lodsb
    or al, al
    jz .done_real
    mov ah, 0x0E  
    int 0x10
    jmp print_string_real_mode
.done_real:
    ret

wait_for_keypress:
    xor ax, ax
    int 0x16
    ret

print_string:
    lodsb
    test al, al
    jz .done_pm
    mov ah, 0x07
    stosw
    jmp print_string
.done_pm:
    ret

msg_real_mode db 'Real Mode: Press any key to enter Protected Mode...', 0
msg_protected_mode db 'Protected Mode: Hello World!', 0

align 8
gdt:
    dq 0x0000000000000000 
    dq 0x00CF9A000000FFFF 
    dq 0x00CF92000000FFFF 

gdt_descriptor:
    dw gdt_end - gdt - 1
    dd gdt
gdt_end:

CODE_SEL equ 0x08
DATA_SEL equ 0x10

times 510 - ($ - $$) db 0
dw 0xAA55

;nasm -f bin -o main.bin main.asm
;qemu-system-x86_64 -drive format=raw,file=main.bin