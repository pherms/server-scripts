import unittest
import modules as mods

class Testing(unittest.TestCase):
    def test_isDirectory(self):
        isDirectory = mods.isDirectory("/etc")
        self.assertTrue(isDirectory)

if __name__ == '__main__':
    unittest.main()