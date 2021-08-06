import subprocess
import unittest
from typing import List


class TestCompilation(unittest.TestCase):
    def tearDown(self):
        self._remove_program()

    def test_example_1(self):
        self._test_successful_execution("test1.tig", 0)

    def test_example_2(self):
        self._test_successful_execution("test2.tig", 0)

    def test_example_3(self):
        self._test_successful_execution("test3.tig", 0)

    def test_example_4(self):
        self._test_successful_execution("test4.tig", 0)

    def test_example_5(self):
        self._test_successful_execution("test5.tig", 0)

    def test_example_6(self):
        self._test_segmentation_fault("test6.tig")

    def test_example_7(self):
        self._test_segmentation_fault("test7.tig")

    def test_example_8(self):
        self._test_successful_execution("test8.tig", 40)

    def test_example_9(self):
        self._test_compilation_error("test9.tig")

    def test_example_10(self):
        self._test_compilation_error("test10.tig")

    def test_example_11(self):
        self._test_compilation_error("test11.tig")

    def test_example_12(self):
        self._test_successful_execution("test12.tig", 0)

    def test_example_13(self):
        self._test_compilation_error("test13.tig")

    def test_example_14(self):
        self._test_compilation_error("test14.tig")

    def test_example_15(self):
        self._test_compilation_error("test15.tig")

    def test_example_16(self):
        self._test_compilation_error("test16.tig")

    def test_example_17(self):
        self._test_compilation_error("test17.tig")

    def test_example_18(self):
        self._test_compilation_error("test18.tig")

    def test_example_19(self):
        self._test_compilation_error("test19.tig")

    def test_example_20(self):
        self._test_compilation_error("test20.tig")

    def test_example_21(self):
        self._test_compilation_error("test21.tig")

    def test_example_22(self):
        self._test_compilation_error("test22.tig")

    def test_example_23(self):
        self._test_compilation_error("test23.tig")

    def test_example_24(self):
        self._test_compilation_error("test24.tig")

    def test_example_25(self):
        self._test_compilation_error("test25.tig")

    def test_example_26(self):
        self._test_compilation_error("test26.tig")

    def test_example_27(self):
        self._test_successful_execution("test27.tig", 2)

    def test_example_28(self):
        self._test_compilation_error("test28.tig")

    def test_example_29(self):
        self._test_compilation_error("test29.tig")

    def test_example_30(self):
        self._test_successful_execution("test30.tig", 0)

    def test_example_31(self):
        self._test_compilation_error("test31.tig")

    def test_example_32(self):
        self._test_compilation_error("test32.tig")

    def test_example_33(self):
        self._test_compilation_error("test33.tig")

    def test_example_34(self):
        self._test_compilation_error("test34.tig")

    def test_example_35(self):
        self._test_compilation_error("test35.tig")

    def test_example_36(self):
        self._test_compilation_error("test36.tig")

    def test_example_37(self):
        self._test_successful_execution("test37.tig", 0)

    def test_example_38(self):
        self._test_compilation_error("test38.tig")

    def test_example_39(self):
        self._test_compilation_error("test39.tig")

    def test_example_40(self):
        self._test_compilation_error("test40.tig")

    def test_example_41(self):
        self._test_successful_execution("test41.tig", 0)

    def test_example_42(self):
        self._test_successful_execution("test42.tig", 0)

    def test_example_43(self):
        self._test_compilation_error("test43.tig")

    def test_example_44(self):
        self._test_successful_execution("test44.tig", 0)

    def test_example_45(self):
        self._test_compilation_error("test45.tig")

    def test_example_46(self):
        self._test_successful_execution("test46.tig", 0)

    def test_example_47(self):
        self._test_successful_execution("test47.tig", 0)

    def test_example_48(self):
        self._test_successful_execution("test48.tig", 0)

    def test_example_49(self):
        self._test_compilation_error("test49.tig")

    def test_example_50(self):
        self._test_successful_execution("test50.tig", 1)

    def test_example_51(self):
        self._test_successful_execution("test51.tig", 0)

    def test_example_52(self):
        self._test_successful_execution("test52.tig", 1)

    def test_example_53(self):
        self._test_successful_execution("test53.tig", 0)

    def test_example_54(self):
        self._test_successful_execution("test54.tig", 0)

    def test_example_55(self):
        self._test_successful_execution("test55.tig", 0)

    def test_example_56(self):
        self._test_successful_execution("test56.tig", 0)

    def test_example_57(self):
        self._test_successful_execution("test57.tig", 0)

    def test_example_58(self):
        self._test_successful_execution("test58.tig", 4)

    def test_example_59(self):
        self._test_successful_execution("test59.tig", 1)

    def test_example_60(self):
        self._test_successful_execution("test60.tig", 0)

    def test_example_61(self):
        self._test_successful_execution("test61.tig", 0)

    def test_example_62(self):
        self._test_successful_execution("test62.tig", 0)

    def test_example_63(self):
        self._test_successful_execution("test63.tig", 0)

    def test_example_64(self):
        self._test_successful_execution("test64.tig", 10)

    def test_example_65(self):
        self._test_successful_execution("test65.tig", 101)

    def test_example_66(self):
        self._test_successful_execution("test66.tig", 42)

    def test_example_67(self):
        self._test_successful_execution("test67.tig", 0)

    def test_example_merge(self):
        self._compile_program("merge.tig")
        result = self._run_compiled_program(input="1 3 5 6 7 10; 0 2 4 8 9;")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "0 1 2 3 4 5 6 7 8 9 10")

    def test_example_queens(self):
        self._compile_program("queens.tig")
        result = self._run_compiled_program()

        self.assertEqual(result.returncode, 0)
        self.assertIn(
            " O . . . . . . .\n"
            + " . . . . O . . .\n"
            + " . . . . . . . O\n"
            + " . . . . . O . .\n"
            + " . . O . . . . .\n"
            + " . . . . . . O .\n"
            + " . O . . . . . .\n"
            + " . . . O . . . .",
            result.stdout,
        )

    def _test_compilation_error(self, source_file_name: str):
        compilation_result = self._compile_program(source_file_name)
        self.assertIn("error", compilation_result.stdout)

        ls_result = self._run_command(["ls"])
        self.assertNotIn("a.out", ls_result.stdout)

    def _test_successful_execution(self, source_file_name: str, return_code: int):
        self._compile_program(source_file_name)
        result = self._run_compiled_program()

        self.assertEqual(result.returncode, return_code)

    def _test_segmentation_fault(self, source_file_name: str):
        self._compile_program(source_file_name)
        result = self._run_compiled_program()

        self.assertEqual(result.returncode, -11)

    def _compile_program(self, source_file_name: str) -> subprocess.CompletedProcess:
        return self._run_command(["./compile.sh", "examples/" + source_file_name])

    def _run_compiled_program(self, **kwargs) -> subprocess.CompletedProcess:
        return self._run_command(["./a.out"], **kwargs)

    def _remove_program(self):
        self._run_command(["rm", "a.out"])

    def _run_command(
        self, arguments: List[str], **kwargs
    ) -> subprocess.CompletedProcess:
        return subprocess.run(
            arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            **kwargs
        )
