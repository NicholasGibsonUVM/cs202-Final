  .globl main
g_funstart:
  movq %rdi, %rdx
  movq %rdx, %r11
  movq 16(%r11), %rdx
  movq %rdx, %rax
  jmp g_funconclusion
g_fun:
  pushq %rbp
  movq %rsp, %rbp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14
  subq $0, %rsp
  jmp g_funstart
g_funconclusion:
  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
f_funlabel_14:
  movq free_ptr(%rip), %rdx
  addq $24, free_ptr(%rip)
  movq %rdx, %r11
  movq $5, 0(%r11)
  movq %rdx, %r11
  movq %r12, 8(%r11)
  movq %rdx, %r11
  movq %rbx, 16(%r11)
  leaq g(%rip), %rdx
  movq %rdx, %r11
  movq 8(%r11), %rcx
  movq %rdx, %rdi
  callq *%rcx
  movq %rax, %rdx
  movq %rdx, %rax
  jmp f_funconclusion
f_funlabel_15:
  jmp f_funlabel_14
f_funlabel_16:
  movq %r15, %rdi
  movq $24, %rsi
  callq collect
  jmp f_funlabel_14
f_funstart:
  movq %rdi, %rdx
  movq $3, %rbx
  movq free_ptr(%rip), %rax
  addq $24, %rax
  movq %rax, %rdx
  cmpq fromspace_end(%rip), %rdx
  setl %al
  movzbq %al, %rdx
  movq $1, %rax
  cmpq %rdx, %rax
  je f_funlabel_15
  jmp f_funlabel_16
f_fun:
  pushq %rbp
  movq %rsp, %rbp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14
  subq $0, %rsp
  jmp f_funstart
f_funconclusion:
  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
mainlabel_11:
  movq free_ptr(%rip), %rdx
  addq $16, free_ptr(%rip)
  movq %rdx, %r11
  movq $3, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  leaq f(%rip), %rcx
  movq %rcx, %r11
  movq 8(%r11), %rdx
  movq %rcx, %rdi
  callq *%rdx
  movq %rax, %rdx
  movq %rdx, %rdi
  callq print_int
  movq $0, %rax
  jmp mainconclusion
mainlabel_12:
  jmp mainlabel_11
mainlabel_13:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp mainlabel_11
mainstart:
  movq $5, %rdx
  movq free_ptr(%rip), %rax
  addq $16, %rax
  movq %rax, %rdx
  cmpq fromspace_end(%rip), %rdx
  setl %al
  movzbq %al, %rdx
  movq $1, %rax
  cmpq %rdx, %rax
  je mainlabel_12
  jmp mainlabel_13
main:
  pushq %rbp
  movq %rsp, %rbp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14
  subq $0, %rsp
  movq $16384, %rdi
  movq $16, %rsi
  callq initialize
  movq rootstack_begin(%rip), %r15
  jmp mainstart
mainconclusion:
  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
