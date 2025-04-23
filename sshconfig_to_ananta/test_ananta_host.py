import tempfile
import unittest
from pathlib import Path

from ananta_host import AnantaHost


class TestAnantaHost(unittest.TestCase):
    def test_valid_host_minimal(self):
        host = AnantaHost(
            alias="test-host",
            ip="192.168.1.1",
            port="",
            username="",
            key_path="",
            tags=[],
            relocate=None,
        )
        self.assertEqual(host.alias, "test-host")
        self.assertEqual(host.ip, "192.168.1.1")
        self.assertEqual(host.port, 22)
        self.assertEqual(host.username, "root")
        self.assertEqual(host.key_path, "#")
        self.assertEqual(host.tags, [])

    def test_valid_host_full(self):
        with tempfile.NamedTemporaryFile() as tf:
            host = AnantaHost(
                alias="db-host",
                ip="10.0.0.2",
                port="2222",
                username="ubuntu",
                key_path=tf.name,
                tags=["db", "prod"],
                relocate=None,
            )
            self.assertEqual(host.port, 2222)
            self.assertEqual(host.username, "ubuntu")
            self.assertEqual(host.key_path, tf.name)
            self.assertEqual(host.tags, ["db", "prod"])

    def test_port_validation(self):
        # Port too large
        with self.assertRaises(ValueError):
            AnantaHost("h", "1.1.1.1", "99999", "u", "#", [], None)
        # Negative port
        with self.assertRaises(ValueError):
            AnantaHost("h", "1.1.1.1", "-22", "u", "#", [], None)
        # Port zero
        with self.assertRaises(ValueError):
            AnantaHost("h", "1.1.1.1", "0", "u", "#", [], None)
        # Non-numeric port
        with self.assertRaises(ValueError):
            AnantaHost("h", "1.1.1.1", "abc", "u", "#", [], None)

    def test_empty_alias_or_ip(self):
        with self.assertRaises(ValueError):
            AnantaHost("", "1.1.1.1", "22", "u", "#", [], None)
        with self.assertRaises(ValueError):
            AnantaHost("host", "", "22", "u", "#", [], None)

    def test_key_path_relocation_success(self):
        with tempfile.NamedTemporaryFile() as tf:
            relocated_file = Path(tf.name)
            relocated_dir = relocated_file.parent.resolve(strict=True)
            relocated_file = relocated_dir / relocated_file.name
            host = AnantaHost(
                alias="test",
                ip="1.2.3.4",
                port="22",
                username="user",
                key_path=tf.name,
                tags=[],
                relocate=relocated_dir,
            )
            self.assertEqual(host.key_path, str(relocated_file))

    def test_key_path_relocation_failure(self):
        with self.assertRaises(FileNotFoundError):
            AnantaHost(
                alias="test",
                ip="1.2.3.4",
                port="22",
                username="user",
                key_path="/nonexistent/key.pem",
                tags=[],
                relocate=Path("/tmp"),
            )

    def test_to_string_methods(self):
        with tempfile.NamedTemporaryFile() as tf:
            relocated_key = Path(tf.name).resolve(strict=True)
            relocate = relocated_key.parent
            host = AnantaHost(
                alias="web",
                ip="10.0.0.1",
                port="22",
                username="admin",
                key_path=f"/not-exist/{tf.name}",
                tags=["web", "dev"],
                relocate=relocate,
            )
            self.assertEqual(
                host.to_string(),
                f"web,10.0.0.1,22,admin,{relocated_key},web:dev\n",
            )
            self.assertEqual(
                host.to_string_with_fields(),
                f"  alias:    web\n"
                f"  ip:       10.0.0.1\n"
                f"  port:     22\n"
                f"  username: admin\n"
                f"  key_path: {relocated_key}\n"
                f"  tags:     web,dev\n",
            )


if __name__ == "__main__":
    unittest.main()
