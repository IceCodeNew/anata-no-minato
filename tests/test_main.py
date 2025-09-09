#!/usr/bin/env python3
# pyright: strict

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

from sshconfig_to_ananta.main import main, parse_arguments


class TestMain(unittest.TestCase):
    def test_parse_arguments_defaults(self):
        """Test parse_arguments with default values."""
        with patch.object(sys, "argv", ["main.py", "output.csv"]):
            args = parse_arguments()

            self.assertEqual(args.ssh, Path.home() / ".ssh" / "config")
            self.assertEqual(args.server_list, Path("output.csv"))
            self.assertIsNone(args.relocate)

    def test_parse_arguments_with_custom_paths(self):
        """Test parse_arguments with custom paths."""
        with patch.object(
            sys,
            "argv",
            [
                "main.py",
                "--ssh",
                "/custom/ssh/config",
                "--relocate",
                "/custom/relocate",
                "output.csv",
            ],
        ):
            args = parse_arguments()

            self.assertEqual(args.ssh, Path("/custom/ssh/config"))
            self.assertEqual(args.server_list, Path("output.csv"))
            self.assertEqual(args.relocate, Path("/custom/relocate"))

    def test_parse_arguments_with_toml_extension(self):
        """Test parse_arguments with TOML output file."""
        with patch.object(sys, "argv", ["main.py", "output.toml"]):
            args = parse_arguments()

            self.assertEqual(args.server_list, Path("output.toml"))

    @patch("sshconfig_to_ananta.main.convert_to_ananta_hosts")
    @patch("sshconfig_to_ananta.main.tomli_w", None)
    @patch("builtins.open", new_callable=mock_open)
    def test_main_csv_output(self, mock_file, mock_convert):
        """Test main function with CSV output."""
        # Mock the convert function to return empty list
        mock_convert.return_value = []

        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            # Mock sys.argv
            test_args = ["main.py", str(temp_path)]
            with patch.object(sys, "argv", test_args):
                main()

            # Verify convert_to_ananta_hosts was called
            mock_convert.assert_called_once()

            # Verify file was opened for writing
            mock_file.assert_called_once_with(temp_path, "w", encoding="utf-8")

        finally:
            # Clean up
            if temp_path.exists():
                temp_path.unlink()

    @patch("sshconfig_to_ananta.main.convert_to_ananta_hosts")
    @patch("sshconfig_to_ananta.main.tomli_w")
    @patch("builtins.open", new_callable=mock_open)
    def test_main_toml_output(self, mock_file, mock_tomli_w, mock_convert):
        """Test main function with TOML output."""
        # Mock the convert function to return empty list
        mock_convert.return_value = []

        # Create a temporary file with .toml extension for testing
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".toml", delete=False
        ) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            # Mock sys.argv
            test_args = ["main.py", str(temp_path)]
            with patch.object(sys, "argv", test_args):
                main()

            # Verify convert_to_ananta_hosts was called
            mock_convert.assert_called_once()

            # Verify toml dump was called
            mock_tomli_w.dump.assert_called_once()

        finally:
            # Clean up
            if temp_path.exists():
                temp_path.unlink()

    @patch("sshconfig_to_ananta.main.convert_to_ananta_hosts")
    @patch("sshconfig_to_ananta.main.tomli_w")
    @patch("builtins.open", new_callable=mock_open)
    def test_main_auto_add_toml_extension(self, mock_file, mock_tomli_w, mock_convert):
        """Test main function auto-adds .toml extension when toml_w is available."""
        # Mock the convert function to return empty list
        mock_convert.return_value = []

        # Create a temporary file with .csv extension
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            # Mock sys.argv
            test_args = ["main.py", str(temp_path)]
            with patch.object(sys, "argv", test_args):
                main()

            # Verify file was opened with .toml extension
            expected_path = temp_path.with_suffix(".toml")
            mock_file.assert_called_once_with(expected_path, "wb")

        finally:
            # Clean up
            if temp_path.exists():
                temp_path.unlink()

    @patch("sshconfig_to_ananta.main.convert_to_ananta_hosts")
    @patch("sshconfig_to_ananta.main.tomli_w", None)
    @patch("builtins.open", new_callable=mock_open)
    def test_main_csv_output_no_toml_extension_change(self, mock_file, mock_convert):
        """Test main function doesn't change extension when toml_w is not available."""
        # Mock the convert function to return empty list
        mock_convert.return_value = []

        # Create a temporary file with .toml extension
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".toml", delete=False
        ) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            # Mock sys.argv
            test_args = ["main.py", str(temp_path)]
            with patch.object(sys, "argv", test_args):
                main()

            # Verify file was opened with original .toml extension
            mock_file.assert_called_once_with(temp_path, "w", encoding="utf-8")

        finally:
            # Clean up
            if temp_path.exists():
                temp_path.unlink()

    @patch("sshconfig_to_ananta.main.convert_to_ananta_hosts")
    def test_main_convert_exception(self, mock_convert):
        """Test main function handles convert_to_ananta_hosts exception."""
        # Mock the convert function to raise an exception
        mock_convert.side_effect = Exception("Conversion failed")

        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            # Mock sys.argv
            test_args = ["main.py", str(temp_path)]
            with patch.object(sys, "argv", test_args):
                with self.assertRaises(SystemExit) as cm:
                    main()

                # Verify it exits with code 1
                self.assertEqual(cm.exception.code, 1)

        finally:
            # Clean up
            if temp_path.exists():
                temp_path.unlink()

    @patch("sshconfig_to_ananta.main.convert_to_ananta_hosts")
    @patch("sshconfig_to_ananta.main.tomli_w", None)
    @patch("builtins.open", new_callable=mock_open)
    def test_main_write_exception(self, mock_file, mock_convert):
        """Test main function handles file write exception."""
        # Mock the convert function to return empty list
        mock_convert.return_value = []

        # Mock open to raise an exception
        mock_file.side_effect = IOError("Write failed")

        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            # Mock sys.argv
            test_args = ["main.py", str(temp_path)]
            with patch.object(sys, "argv", test_args):
                with self.assertRaises(IOError):
                    main()

        finally:
            # Clean up
            if temp_path.exists():
                temp_path.unlink()

    def test_main_relocate_directory_not_exists(self):
        """Test main function with non-existent relocate directory."""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_path = Path(temp_file.name)

        try:
            # Mock sys.argv with non-existent relocate path
            test_args = ["main.py", "--relocate", "/nonexistent/path", str(temp_path)]
            with patch.object(sys, "argv", test_args):
                with self.assertRaises(FileNotFoundError):
                    main()

        finally:
            # Clean up
            if temp_path.exists():
                temp_path.unlink()

    @patch("sshconfig_to_ananta.main.convert_to_ananta_hosts")
    @patch("sshconfig_to_ananta.main.tomli_w", None)
    @patch("builtins.open", new_callable=mock_open)
    def test_main_relocate_directory_exists(self, mock_file, mock_convert):
        """Test main function with existing relocate directory."""
        # Mock the convert function to return empty list
        mock_convert.return_value = []

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a temporary file for testing
            with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
                temp_path = Path(temp_file.name)

            try:
                # Mock sys.argv with existing relocate path
                test_args = ["main.py", "--relocate", temp_dir, str(temp_path)]
                with patch.object(sys, "argv", test_args):
                    main()

                # Verify convert_to_ananta_hosts was called with relocate path
                mock_convert.assert_called_once()
                args = mock_convert.call_args[0]
                self.assertEqual(args[1], Path(temp_dir).resolve())

            finally:
                # Clean up
                if temp_path.exists():
                    temp_path.unlink()


if __name__ == "__main__":
    unittest.main()
