import unittest
from typing import List

import intermediate_representation.tree as irt
from canonical.basic_block import basic_block, BasicBlock

from canonical.linearize import linearize
from intermediate_representation.fragment import FragmentManager, ProcessFragment
from tests.utils.compilation_steps import semantic_analysis


class TestBasicBlock(unittest.TestCase):
    """Checks that every basic block starts with a label, ends with a jump and has no labels or
    jumps in the middle. It also determines whether all original statements are in one block."""

    def setUp(self):
        FragmentManager.fragment_list = []

    def test_example_1(self):
        self._build_basic_blocks("test1.tig")

    def test_example_2(self):
        self._build_basic_blocks("test2.tig")

    def test_example_3(self):
        self._build_basic_blocks("test3.tig")

    def test_example_4(self):
        self._build_basic_blocks("test4.tig")

    def test_example_5(self):
        self._build_basic_blocks("test5.tig")

    def test_example_6(self):
        self._build_basic_blocks("test6.tig")

    def test_example_7(self):
        self._build_basic_blocks("test7.tig")

    def test_example_8(self):
        self._build_basic_blocks("test8.tig")

    def test_example_12(self):
        self._build_basic_blocks("test12.tig")

    def test_example_27(self):
        self._build_basic_blocks("test27.tig")

    def test_example_30(self):
        self._build_basic_blocks("test30.tig")

    def test_example_37(self):
        self._build_basic_blocks("test37.tig")

    def test_example_41(self):
        self._build_basic_blocks("test41.tig")

    def test_example_42(self):
        self._build_basic_blocks("test42.tig")

    def test_example_44(self):
        self._build_basic_blocks("test44.tig")

    def test_example_46(self):
        self._build_basic_blocks("test46.tig")

    def test_example_47(self):
        self._build_basic_blocks("test47.tig")

    def test_example_48(self):
        self._build_basic_blocks("test48.tig")

    def test_example_50(self):
        self._build_basic_blocks("test50.tig")

    def test_example_51(self):
        self._build_basic_blocks("test51.tig")

    def test_example_52(self):
        self._build_basic_blocks("test52.tig")

    def test_example_53(self):
        self._build_basic_blocks("test53.tig")

    def test_example_54(self):
        self._build_basic_blocks("test54.tig")

    def test_example_55(self):
        self._build_basic_blocks("test55.tig")

    def test_example_56(self):
        self._build_basic_blocks("test56.tig")

    def test_example_57(self):
        self._build_basic_blocks("test57.tig")

    def test_example_58(self):
        self._build_basic_blocks("test58.tig")

    def test_example_59(self):
        self._build_basic_blocks("test59.tig")

    def test_example_60(self):
        self._build_basic_blocks("test60.tig")

    def test_example_61(self):
        self._build_basic_blocks("test61.tig")

    def test_example_62(self):
        self._build_basic_blocks("test62.tig")

    def test_example_63(self):
        self._build_basic_blocks("test63.tig")

    def test_example_64(self):
        self._build_basic_blocks("test64.tig")

    def test_example_65(self):
        self._build_basic_blocks("test65.tig")

    def test_example_66(self):
        self._build_basic_blocks("test66.tig")

    def test_example_merge(self):
        self._build_basic_blocks("merge.tig")

    def test_example_queens(self):
        self._build_basic_blocks("queens.tig")

    def _build_basic_blocks(self, file_name: str):
        semantic_analysis(file_name)
        for fragment in FragmentManager.get_fragments():
            if isinstance(fragment, ProcessFragment):
                linear_statements = linearize(fragment.body)
                blocked_statements = basic_block(linear_statements)
                self._assert_block_structure(blocked_statements)
                self._assert_statements_were_not_removed(
                    linear_statements, blocked_statements
                )

    def _assert_block_structure(self, block: BasicBlock):
        for statement_list in block.statement_lists:
            self.assertIsInstance(statement_list[0], irt.Label)
            self.assertIsInstance(statement_list[-1], (irt.Jump, irt.ConditionalJump))
            for middle_statement in statement_list[1:-1]:
                self.assertNotIsInstance(
                    middle_statement, (irt.Label, irt.Jump, irt.ConditionalJump)
                )

    def _assert_statements_were_not_removed(
        self, linear_statements: List[irt.Statement], block: BasicBlock
    ):
        flattened_block = [
            statement
            for statement_list in block.statement_lists
            for statement in statement_list
        ]
        for statement in linear_statements:
            self.assertIn(statement, flattened_block)
