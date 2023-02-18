import unittest
import auth

class TestAuth(unittest.TestCase):

    def test_jwt(self):
        self.assertEqual(auth.test_jwt("User1", "secret_keyyy"), "User1") # devrait toujours être vrai, test de la librairie jwt
        self.assertEqual(auth.test_jwt("blob", "secret_keyyy"), "blob")

if __name__ == '__main__':
    unittest.main()