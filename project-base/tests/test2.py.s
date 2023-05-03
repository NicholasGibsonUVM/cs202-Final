  .globl main
fact_funlabel_15:
  movq $0, %rax
  jmp fact_funconclusion
fact_funlabel_16:
  movq $1, %rax
  jmp fact_funconclusion
fact_funlabel_17:
  movq %rbx, %rax
  subq $1, %rax
  movq %rax, %rsi
  movq %rdx, %rdx
  movq %rdx, %r11
  movq 8(%r11), %rcx
  movq %rsi, %rdi
  movq %rdx, %rsi
  callq *%rcx
  movq %rax, %rdx
  movq %rbx, %rax
  imulq %rdx, %rax
  movq %rax, %rdx
  movq %rdx, %rax
  jmp fact_funconclusion
fact_funstart:
  movq %rdi, %rbx
  movq %rsi, %rdx
  cmpq $0, %rbx
  sete %al
  movzbq %al, %rcx
  movq $1, %rax
  cmpq %rcx, %rax
  je fact_funlabel_16
  jmp fact_funlabel_17
fact_fun:
  pushq %rbp
  movq %rsp, %rbp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14
  subq $0, %rsp
  jmp fact_funstart
fact_funconclusion:
  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
mainlabel_12:
  movq free_ptr(%rip), %rdx
  addq $16, free_ptr(%rip)
  movq %rdx, %r11
  movq $3, 0(%r11)
  leaq fact_fun(%rip), %rcx
  movq %rdx, %r11
  movq %rcx, 8(%r11)
  movq %rdx, %rcx
  movq %rcx, %r11
  movq 8(%r11), %rdx
  movq $5, %rdi
  movq %rcx, %rsi
  callq *%rdx
  movq %rax, %rdx
  movq %rdx, %rdi
  callq print_int
  movq $0, %rax
  jmp mainconclusion
mainlabel_13:
  jmp mainlabel_12
mainlabel_14:
  movq %r15, %rdi
  movq $16, %rsi
  callq collect
  jmp mainlabel_12
mainstart:
  movq free_ptr(%rip), %rax
  addq $16, %rax
  movq %rax, %rdx
  cmpq fromspace_end(%rip), %rdx
  setl %al
  movzbq %al, %rdx
  movq $1, %rax
  cmpq %rdx, %rax
  je mainlabel_13
  jmp mainlabel_14
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
