from typing import Set, Dict, Tuple
import sys
import traceback

from cs202_support.python import *
import cs202_support.x86 as x86
import constants
import cfun
import print_x86defs
from interference_graph import InterferenceGraph

comparisons = ['eq', 'gt', 'gte', 'lt', 'lte']
gensym_num = 0
global_logging = False

global_values = ['free_ptr', 'fromspace_end']

tuple_var_types = {}
function_names = set()
function_envs = {}  # Used for lexical scoping

def log(label, value):
    if global_logging:
        print()
        print(f'--------------------------------------------------')
        print(f'Logging: {label}')
        print(value)
        print(f'--------------------------------------------------')


def log_ast(label, value):
    log(label, print_ast(value))


def gensym(x):
    """
    Constructs a new variable name guaranteed to be unique.
    :param x: A "base" variable name (e.g. "x")
    :return: A unique variable name (e.g. "x_1")
    """

    global gensym_num
    gensym_num = gensym_num + 1
    return f'{x}_{gensym_num}'


##################################################
# typecheck
##################################################
# op     ::= "add" | "sub" | "mult" | "not" | "or" | "and" | "eq" | "gt" | "gte" | "lt" | "lte"
#          | "tuple" | "subscript"
# Expr   ::= Var(x) | Constant(n) | Prim(op, List[Expr]) | Begin(Stmts, Expr)
#          | Call(Expr, List[Expr]) | Lambda(List[Tuple[str, type]], Expr) 
# Stmt   ::= Assign(x, Expr) | Print(Expr) | If(Expr, Stmts, Stmts) | While(Expr, Stmts)
#          | Return(Expr) | FunctionDef(str, List[Tuple[str, type]], List[Stmt], type)
#          | AnnAssign(Var, Type, Expr, 0)
# Stmts  ::= List[Stmt]
# LFun   ::= Program(Stmts)

@dataclass
class Callable:
    args: List[type]
    output_type: type


TEnv = Dict[str, Callable | Tuple | type]


def typecheck(program: Program) -> Program:
    """
    Typechecks the input program; throws an error if the program is not well-typed.
    :param program: The Ltup program to typecheck
    :return: The program, if it is well-typed
    """

    pass

def uniquify(program: Program) -> Program:
    """
    Ensures the every parameter in every function definition is unique.
    """
    def uniquify_stmt(stmt: Stmt, env) -> Stmt:
        match stmt:
            case Assign(x, expr):
                pass
            case FunctionDef(name, params, body, return_type):
                new_params = [(gensym(param[0]), param[1]) for param in params]
                return FunctionDef(name, new_params, body, return_type)
            # case AnnAssign():
            #     pass
            case _:
                return stmt
            
    new_stmts = []
    for stmt in program.stmts:
        new_stmts.append(uniquify_stmt(stmt), env)
    return Program(new_stmts)

def convert_assignments(program: Program) -> Program:
    AF: set(str) = set()

    def assigned_var_stmt(stmt: Stmt, env: TEnv) -> Tuple(set(str), set(str)):
        """
        returns the set of variables that
        occur in the left-hand side of an assignment statement 
        and otherwise returns the empty set.
        """
        assigned_vars = set()
        free_vars = set()
        match stmt:
            case FunctionDef(name, params, body, return_type):
                for statement in body:
                    if isinstance(statement, Assign| AnnAssign):
                        assigned_vars.add(statement.name)
                        free_vars.add(free_variables(statement.rhs, [param[0] for param in params]))
                return assigned_vars, free_vars
            case _:
                return set(), set()

    def free_variables(expr: Expr, params: List[str, type]) -> set(str):
        """
        returns the set of variables that occur free in expr.
        """
        match expr:
                case Var(x):
                    if x in params:
                        return set()
                    else:
                        return set(x)
                case Constant(n):
                    return set()
                case Prim(op, args):
                    return set([arg for arg in args if arg not in params])
                case Lambda(lambda_params, body):
                    return free_variables(body, lambda_params)

    for stmt in program.stmts:
        assigned_vars, free_vars = assigned_var_stmt(stmt)
        AF += free_vars.union(assigned_vars)
                
    


##################################################
# remove-complex-opera*
##################################################
# op     ::= "add" | "sub" | "mult" | "not" | "or" | "and" | "eq" | "gt" | "gte" | "lt" | "lte"
#          | "tuple" | "subscript"
# Expr   ::= Var(x) | Constant(n) | Prim(op, List[Expr])
#          | Call(Expr, List[Expr])
# Stmt   ::= Assign(x, Expr) | Print(Expr) | If(Expr, Stmts, Stmts) | While(Expr, Stmts)
#          | Return(Expr) | FunctionDef(str, List[Tuple[str, type]], List[Stmt], type)
# Stmts  ::= List[Stmt]
# LFun   ::= Program(Stmts)

def rco(prog: Program) -> Program:
    """
    Removes complex operands. After this pass, the arguments to operators (unary and binary
    operators, and function calls like "print") will be atomic.
    :param prog: An Ltup program
    :return: An Ltup program with atomic operator arguments.
    """

    pass


##################################################
# expose-allocation
##################################################
# op     ::= "add" | "sub" | "mult" | "not" | "or" | "and" | "eq" | "gt" | "gte" | "lt" | "lte"
#          | "tuple" | "subscript"
# Expr   ::= Var(x) | Constant(n) | Prim(op, List[Expr])
#          | Call(Expr, List[Expr])
# Stmt   ::= Assign(x, Expr) | Print(Expr) | If(Expr, Stmts, Stmts) | While(Begin(Stmts, Expr), Stmts)
#          | Return(Expr) | FunctionDef(str, List[Tuple[str, type]], List[Stmt], type)
# Stmts  ::= List[Stmt]
# LFun   ::= Program(Stmts)

def expose_alloc(prog: Program) -> Program:
    """
    Exposes allocations in an Ltup program. Replaces tuple(...) with explicit
    allocation.
    :param prog: An Ltup program
    :return: An Ltup program, without Tuple constructors
    """

    pass


##################################################
# explicate-control
##################################################
# op     ::= "add" | "sub" | "mult" | "not" | "or" | "and" | "eq" | "gt" | "gte" | "lt" | "lte"
#          | "subscript" | "allocate" | "collect" | "tuple_set"
# Atm    ::= Var(x) | Constant(n)
# Expr   ::= Atm | Prim(op, List[Expr])
#          | Call(Expr, List[Expr])
# Stmt   ::= Assign(x, Expr) | Print(Expr) | If(Expr, Stmts, Stmts) | While(Begin(Stmts, Expr), Stmts)
#          | Return(Expr) | FunctionDef(str, List[Tuple[str, type]], List[Stmt], type)
# Stmts  ::= List[Stmt]
# LFun   ::= Program(Stmts)

def explicate_control(prog: Program) -> cfun.CProgram:
    """
    Transforms an Ltup Expression into a Ctup program.
    :param prog: An Ltup Expression
    :return: A Ctup Program
    """

    # the basic blocks of the program
    basic_blocks: Dict[str, List[cfun.Stmt]] = {}
    functions: List[cfun.CFunctionDef] = []
    current_function = 'main'

    pass


##################################################
# select-instructions
##################################################
# op           ::= "add" | "sub" | "mult" | "not" | "or" | "and" | "eq" | "gt" | "gte" | "lt" | "lte"
#                | "subscript" | "allocate" | "collect" | "tuple_set"
# Atm          ::= Var(x) | Constant(n)
# Expr         ::= Atm | Prim(op, List[Expr])
# Stmt         ::= Assign(x, Expr) | Print(Expr)
#                | If(Expr, Goto(label), Goto(label)) | Goto(label) | Return(Expr)
# Stmts        ::= List[Stmt]
# CFunctionDef ::= CFunctionDef(name, List[str], Dict[label, Stmts])
# Cfun         ::= CProgram(List[CFunctionDef])

@dataclass(frozen=True, eq=True)
class X86FunctionDef(AST):
    label: str
    blocks: Dict[str, List[x86.Instr]]
    stack_space: Tuple[int, int]

@dataclass(frozen=True, eq=True)
class X86ProgramDefs(AST):
    defs: List[X86FunctionDef]

def select_instructions(prog: cfun.CProgram) -> X86ProgramDefs:
    """
    Transforms a Ltup program into a pseudo-x86 assembly program.
    :param prog: a Ltup program
    :return: a pseudo-x86 program
    """

    current_function = 'main'

    pass


##################################################
# allocate-registers
##################################################
# Arg            ::= Immediate(i) | Reg(r) | ByteReg(r) | Var(x) | Deref(r, offset) | GlobalVal(x)
# op             ::= 'addq' | 'subq' | 'imulq' | 'cmpq' | 'andq' | 'orq' | 'xorq' | 'movq' | 'movzbq'
#                  | 'leaq'
# cc             ::= 'e'| 'g' | 'ge' | 'l' | 'le'
# Instr          ::= NamedInstr(op, List[Arg]) | Callq(label) | Retq()
#                  | Jmp(label) | JmpIf(cc, label) | Set(cc, Arg)
#                  | IndirectCallq(Arg)
# Blocks         ::= Dict[label, List[Instr]]
# X86FunctionDef ::= X86FunctionDef(name, Blocks)
# X86ProgramDefs ::= List[X86FunctionDef]

Color = x86.Arg
Coloring = Dict[x86.Var, x86.Arg]
Saturation = Set[x86.Arg]

def allocate_registers(program: X86ProgramDefs) -> X86ProgramDefs:
    """
    Assigns homes to variables in the input program. Allocates registers and
    stack locations as needed, based on a graph-coloring register allocation
    algorithm.
    :param program: A pseudo-x86 program.
    :return: An x86 program, annotated with the number of bytes needed in stack
    locations.
    """

    pass    


def _allocate_registers(name: str, program: x86.X86Program) -> x86.X86Program:
    pass


##################################################
# patch-instructions
##################################################
# Arg            ::= Immediate(i) | Reg(r) | ByteReg(r) | Var(x) | Deref(r, offset) | GlobalVal(x)
# op             ::= 'addq' | 'subq' | 'imulq' | 'cmpq' | 'andq' | 'orq' | 'xorq' | 'movq' | 'movzbq'
#                  | 'leaq'
# cc             ::= 'e'| 'g' | 'ge' | 'l' | 'le'
# Instr          ::= NamedInstr(op, List[Arg]) | Callq(label) | Retq()
#                  | Jmp(label) | JmpIf(cc, label) | Set(cc, Arg)
#                  | IndirectCallq(Arg)
# Blocks         ::= Dict[label, List[Instr]]
# X86FunctionDef ::= X86FunctionDef(name, Blocks)
# X86ProgramDefs ::= List[X86FunctionDef]

def patch_instructions(program: X86ProgramDefs) -> X86ProgramDefs:
    """
    Patches instructions with two memory location inputs, using %rax as a temporary location.
    :param program: An x86 program.
    :return: A patched x86 program.
    """

    pass


def _patch_instructions(program: x86.X86Program) -> x86.X86Program:
    pass


##################################################
# prelude-and-conclusion
##################################################
# Arg    ::= Immediate(i) | Reg(r) | ByteReg(r) | Deref(r, offset) | GlobalVal(x)
# op     ::= 'addq' | 'subq' | 'imulq' | 'cmpq' | 'andq' | 'orq' | 'xorq' | 'movq' | 'movzbq'
#          | 'leaq'
# cc     ::= 'e'| 'g' | 'ge' | 'l' | 'le'
# Instr  ::= NamedInstr(op, List[Arg]) | Callq(label) | Retq()
#          | Jmp(label) | JmpIf(cc, label) | Set(cc, Arg)
#          | IndirectCallq(Arg)
# Blocks ::= Dict[label, List[Instr]]
# X86    ::= X86Program(Blocks)

def prelude_and_conclusion(program: X86ProgramDefs) -> x86.X86Program:
    """
    Adds the prelude and conclusion for the program.
    :param program: An x86 program.
    :return: An x86 program, with prelude and conclusion.
    """

    pass


def _prelude_and_conclusion(name: str, program: x86.X86Program) -> x86.X86Program:
    pass


##################################################
# Compiler definition
##################################################

compiler_passes = {
    'typecheck': typecheck,
    'remove complex opera*': rco,
    'typecheck2': typecheck,
    'expose allocation': expose_alloc,
    'explicate control': explicate_control,
    'select instructions': select_instructions,
    'allocate registers': allocate_registers,
    'patch instructions': patch_instructions,
    'prelude & conclusion': prelude_and_conclusion,
    'print x86': x86.print_x86
}


def run_compiler(s, logging=False):
    global global_logging

    old_logging = global_logging
    global_logging = logging

    def print_prog(current_program):
        print('Concrete syntax:')
        if isinstance(current_program, x86.X86Program):
            print(x86.print_x86(current_program))
        elif isinstance(current_program, X86ProgramDefs):
            print(print_x86defs.print_x86_defs(current_program))
        elif isinstance(current_program, Program):
            print(print_program(current_program))
        elif isinstance(current_program, cfun.CProgram):
            print(cfun.print_program(current_program))

        print()
        print('Abstract syntax:')
        print(print_ast(current_program))

    current_program = parse(s)

    if logging == True:
        print()
        print('==================================================')
        print(' Input program')
        print('==================================================')
        print()
        print_prog(current_program)

    for pass_name, pass_fn in compiler_passes.items():
        current_program = pass_fn(current_program)

        if logging == True:
            print()
            print('==================================================')
            print(f' Output of pass: {pass_name}')
            print('==================================================')
            print()
            print_prog(current_program)

    global_logging = old_logging
    return current_program


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python compiler.py <source filename>')
    else:
        file_name = sys.argv[1]
        with open(file_name) as f:
            print(f'Compiling program {file_name}...')

            try:
                program = f.read()
                x86_program = run_compiler(program, logging=True)

                with open(file_name + '.s', 'w') as output_file:
                    output_file.write(x86_program)

            except:
                print('Error during compilation! **************************************************')
                traceback.print_exception(*sys.exc_info())

