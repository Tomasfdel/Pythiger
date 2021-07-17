from activation_records.frame import TempMap, temp_to_str
from activation_records.instruction_removal import is_redundant_move
from canonical.canonize import canonize
from intermediate_representation.fragment import FragmentManager, ProcessFragment
from register_allocation.allocation import RegisterAllocator
from semantic_analysis.analyzers import SemanticError, translate_program
from instruction_selection.codegen import Codegen
from lexer import lex as le
from parser import parser as p
import sys
from ply import lex


def main():
    if len(sys.argv) == 1:
        print("Fatal error. No input file detected.")
        return

    f = open(sys.argv[1], "r")
    data = f.read()
    f.close()

    # Lexical Analysis
    lex.input(data)
    try:
        parsed_program = p.parser.parse(data, le.lexer)
    except p.SyntacticError as err:
        print(err)
        return

    # Semantic Analysis and Intermediate Representation Translation
    TempMap.initialize()
    try:
        analysed_program = translate_program(
            parsed_program,
        )
    except SemanticError as err:
        print(err)
        return

    # Canonization
    process_fragments = [
        fragment
        for fragment in FragmentManager.get_fragments()
        if isinstance(fragment, ProcessFragment)
    ]
    canonized_bodies = [canonize(fragment.body) for fragment in process_fragments]

    # Instruction Selection
    assembly_bodies = [
        Codegen.codegen(process_body) for process_body in canonized_bodies
    ]

    print("All good!")
    print(analysed_program.type)
    print("Process fragment amount:", len(canonized_bodies))

    # Register Allocation
    for body, fragment in zip(assembly_bodies, process_fragments):
        allocation_result = RegisterAllocator(fragment.frame).main(body)
        TempMap.update_temp_to_register(allocation_result.temp_to_register)
        instruction_list = [
            instruction
            for instruction in allocation_result.instructions
            if not is_redundant_move(instruction)
        ]
        for instruction in instruction_list:
            print(instruction.format(temp_to_str))
        print("*" * 5)


if __name__ == "__main__":
    main()
