from typing import List

from canonical.basic_block import basic_block
from canonical.linearize import linearize
from canonical.trace import trace_schedule
from intermediate_representation.fragment import FragmentManager, ProcessFragment
from intermediate_representation.tree import Statement


def canonize(statement: Statement) -> List[Statement]:
    return trace_schedule(basic_block(linearize(statement)))


def canonize_process_fragments() -> List[List[Statement]]:
    return [
        canonize(fragment.body)
        for fragment in FragmentManager.get_fragments()
        if isinstance(fragment, ProcessFragment)
    ]
