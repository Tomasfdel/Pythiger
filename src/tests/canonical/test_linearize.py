import unittest
import intermediate_representation.tree as irt

from canonical.linearize import linearize
from intermediate_representation.fragment import FragmentManager, ProcessFragment
from tests.utils.compilation_steps import semantic_analysis


class TestLinearize(unittest.TestCase):
    """Checks that after calling linearize, the resulting statements do not contain any Sequence or
    EvaluateSequence, and that Calls are not subexpressions of binary operations or other function
    calls."""

    def setUp(self):
        FragmentManager.fragment_list = []

    def test_example_1(self):
        self._linearize_trees("test1.tig")

    def test_example_2(self):
        self._linearize_trees("test2.tig")

    def test_example_3(self):
        self._linearize_trees("test3.tig")

    def test_example_4(self):
        self._linearize_trees("test4.tig")

    def test_example_5(self):
        self._linearize_trees("test5.tig")

    def test_example_6(self):
        self._linearize_trees("test6.tig")

    def test_example_7(self):
        self._linearize_trees("test7.tig")

    def test_example_8(self):
        self._linearize_trees("test8.tig")

    def test_example_12(self):
        self._linearize_trees("test12.tig")

    def test_example_27(self):
        self._linearize_trees("test27.tig")

    def test_example_30(self):
        self._linearize_trees("test30.tig")

    def test_example_37(self):
        self._linearize_trees("test37.tig")

    def test_example_41(self):
        self._linearize_trees("test41.tig")

    def test_example_42(self):
        self._linearize_trees("test42.tig")

    def test_example_44(self):
        self._linearize_trees("test44.tig")

    def test_example_46(self):
        self._linearize_trees("test46.tig")

    def test_example_47(self):
        self._linearize_trees("test47.tig")

    def test_example_48(self):
        self._linearize_trees("test48.tig")

    def test_example_50(self):
        self._linearize_trees("test50.tig")

    def test_example_51(self):
        self._linearize_trees("test51.tig")

    def test_example_52(self):
        self._linearize_trees("test52.tig")

    def test_example_53(self):
        self._linearize_trees("test53.tig")

    def test_example_54(self):
        self._linearize_trees("test54.tig")

    def test_example_55(self):
        self._linearize_trees("test55.tig")

    def test_example_56(self):
        self._linearize_trees("test56.tig")

    def test_example_57(self):
        self._linearize_trees("test57.tig")

    def test_example_58(self):
        self._linearize_trees("test58.tig")

    def test_example_59(self):
        self._linearize_trees("test59.tig")

    def test_example_60(self):
        self._linearize_trees("test60.tig")

    def test_example_61(self):
        self._linearize_trees("test61.tig")

    def test_example_62(self):
        self._linearize_trees("test62.tig")

    def test_example_63(self):
        self._linearize_trees("test63.tig")

    def test_example_merge(self):
        self._linearize_trees("merge.tig")

    def test_example_queens(self):
        self._linearize_trees("queens.tig")

    def _linearize_trees(self, file_name: str):
        semantic_analysis(file_name)
        for fragment in FragmentManager.get_fragments():
            if isinstance(fragment, ProcessFragment):
                for linear_statement in linearize(fragment.body):
                    self._assert_no_sequences_statement(linear_statement)

    def _assert_no_sequences_statement(self, statement: irt.Statement):
        self.assertIsInstance(statement, irt.Statement)
        self.assertNotIsInstance(statement, irt.Sequence)

        if isinstance(statement, irt.Jump):
            self._assert_no_sequences_expression(statement.expression)
        elif isinstance(statement, irt.ConditionalJump):
            self._assert_no_sequences_expression(statement.left)
            self._assert_no_sequences_expression(statement.right)
        elif isinstance(statement, irt.Move):
            self._assert_no_sequences_expression(statement.temporary)
            self._assert_no_sequences_expression(statement.expression)
        elif isinstance(statement, irt.StatementExpression):
            self._assert_no_sequences_expression(statement.expression)

    def _assert_no_sequences_expression(self, expression: irt.Expression):
        self.assertIsInstance(expression, irt.Expression)
        self.assertNotIsInstance(expression, irt.EvaluateSequence)

        if isinstance(expression, irt.BinaryOperation):
            self.assertNotIsInstance(expression.left, irt.Call)
            self.assertNotIsInstance(expression.right, irt.Call)
            self._assert_no_sequences_expression(expression.left)
            self._assert_no_sequences_expression(expression.right)
        elif isinstance(expression, irt.Memory):
            self._assert_no_sequences_expression(expression.expression)
        elif isinstance(expression, irt.Call):
            self._assert_no_sequences_expression(expression.function)
            for argument in expression.arguments:
                self.assertNotIsInstance(argument, irt.Call)
                self._assert_no_sequences_expression(argument)
