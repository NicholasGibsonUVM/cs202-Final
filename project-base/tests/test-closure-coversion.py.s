  .globl main
f_funstart:
  movq %rdi, %rdx
  movq %rsi, %rcx
  movq %rcx, %r11
  movq 16(%r11), %rcx
  movq %rdx, %rax
  addq %rcx, %rax
  movq %rax, %rdx
  movq %rdx, %rdx
  movq %rdx, %rax
  jmp f_funconclusion
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
mainlabel_7:
  movq free_ptr(%rip), %rdx
  addq $24, free_ptr(%rip)
  movq %rdx, %r11
  movq $5, 0(%r11)
  leaq f_fun(%rip), %rcx
  movq %rdx, %r11
  movq %rcx, 8(%r11)
  movq %rdx, %r11
  movq %rbx, 16(%r11)
  movq %rdx, %rdx
  movq %rdx, %r11
  movq 8(%r11), %rcx
  movq $3, %rdi
  movq %rdx, %rsi
  callq *%rcx
  movq %rax, %rdx
  movq %rdx, %rdi
  callq print_int
  movq $0, %rax
  jmp mainconclusion
mainlabel_8:
  jmp mainlabel_7
mainlabel_9:
  movq %r15, %rdi
  movq $24, %rsi
  callq collect
  jmp mainlabel_7
mainstart:
  movq $5, %rbx
  movq free_ptr(%rip), %rax
  addq $24, %rax
  movq %rax, %rdx
  cmpq fromspace_end(%rip), %rdx
  setl %al
  movzbq %al, %rdx
  movq $1, %rax
  cmpq %rdx, %rax
  je mainlabel_8
  jmp mainlabel_9
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
