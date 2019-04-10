"""Unit tests for JSON Stringify inversion"""
import os
import unittest
from unittest import mock

with mock.patch.dict("sys.modules", sublime=mock.MagicMock()):
	with mock.patch.dict("sys.modules", sublime_plugin=mock.MagicMock()):
		import json_stringify_command

class TestInvertJSONString(unittest.TestCase):
	"""Unit tests for JSON Stringify inversion"""
	def __init__(self, *args, **kwargs):
		super(TestInvertJSONString, self).__init__(*args, **kwargs)
		self._path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")
		self.maxDiff = None # pylint: disable=invalid-name

	def test_all_inputs(self):
		"""Test each input in ./test_data matches it's corresponding output"""
		for path in os.listdir(self._path):
			path = os.path.join(self._path, path)
			if not os.path.isfile(path) or path.endswith("output.json"):
				continue

			input_data = None
			output_data = None

			with open(path) as in_file:
				input_data = in_file.read()
				input_data = input_data.strip()

			with open(path.replace("input.json", "output.json", 1)) as out_file:
				output_data = out_file.read()
				output_data = output_data.strip()

			inverted_data = json_stringify_command.invert_json_string(input_data)
			self.assertEqual(output_data, inverted_data, "invert_json_string of {} not match expected output".format(path))

if __name__ == "__main__":
	unittest.main()
