# from app import app
#
#
# if __name__ == "__main__":
#     from argparse import ArgumentParser
#
#     parser = ArgumentParser()
#     parser.add_argument(
#         '-p', '--port', default=5000, type=int, help='port to listen on')
#     args = parser.parse_args()
#     port = args.port
#
#     app.run(host='0.0.0.0', port=port)



# class TestUtils(unittest.TestCase):
#
#     def test_is_float(self):
#         self.assertTrue(is_float(5.5))
#         self.assertTrue(is_float(0.6))
#         self.assertFalse(is_float(5))
#         self.assertFalse(is_float('hello'))
#         self.assertFalse(is_float('5.6'))