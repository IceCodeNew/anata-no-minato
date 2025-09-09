#!/usr/bin/env python3
# pyright: strict

import sys
import unittest
from unittest.mock import patch


class TestMainModule(unittest.TestCase):
    def test_main_module_entry_point(self):
        """Test that __main__.py entry point works correctly."""
        # Mock sys.argv with test arguments
        test_args = ["__main__.py", "test_output.csv"]

        with patch.object(sys, "argv", test_args):
            # Mock the main function to avoid actual execution
            with patch("sshconfig_to_ananta.main.main", return_value=None) as mock_main:
                # Import the __main__ module - this should not execute main()
                # because __name__ won't be "__main__" when imported as a module
                import sshconfig_to_ananta.__main__

                # Verify the import worked
                self.assertTrue(hasattr(sshconfig_to_ananta.__main__, "main"))
                # main() should not have been called during import
                mock_main.assert_not_called()

    def test_main_module_imports(self):
        """Test that __main__.py can be imported without errors."""
        try:
            import sshconfig_to_ananta.__main__

            self.assertTrue(hasattr(sshconfig_to_ananta.__main__, "main"))
        except ImportError as e:
            self.fail(f"Failed to import __main__.py: {e}")

    def test_main_module_execution_simulation(self):
        """Test simulating __main__.py execution."""
        # This test verifies that the __main__ module can handle execution
        # The actual if __name__ == "__main__" block is simple and just calls main()

        # Verify that the module imports correctly and has the main function
        import sshconfig_to_ananta.__main__

        self.assertTrue(hasattr(sshconfig_to_ananta.__main__, "main"))

        # The __main__.py file contains: if __name__ == "__main__": main()
        # Since we're importing it as a module, __name__ != "__main__"
        # But we can verify that the structure is correct by checking the source
        import inspect

        source = inspect.getsource(sshconfig_to_ananta.__main__)
        self.assertIn('if __name__ == "__main__"', source)
        self.assertIn("main()", source)

    def test_main_module_direct_execution_simulation(self):
        """Simulate __main__ execution and assert main() is invoked."""
        from runpy import run_module

        with patch("sshconfig_to_ananta.main.main") as mock_main:
            with patch.object(sys, "argv", ["sshconfig_to_ananta.__main__", "out.csv"]):
                run_module("sshconfig_to_ananta.__main__", run_name="__main__")
            mock_main.assert_called_once()


if __name__ == "__main__":
    unittest.main()
