"""
Implementation of json_stringify plugin for Sublime Text 3. It converts between JSON and JSON string representations of data.
"""
import json

# pylint: disable=import-error
# These modules are provided by SublimeText, so they are not going to be installed wherever the linting runs
import sublime
import sublime_plugin
# pylint: enable=import-error

class JsonStringifyCommand(sublime_plugin.TextCommand): # pylint: disable=too-few-public-methods
	"""
	The implementing class for the json_stringify ST3 plugin.

	Converts a selection either from some valid JSON data type to a JSON string or from a JSON
	string to the underlying data structure. The plugin runs on either each selection of text in a
	view, or the entire text of the view.
	"""
	def run(self, edit):
		"""Run the json_stringify plugin"""
		# Do inversion for each selection in view
		for region in self.view.sel():
			if region.size() == 0:
				# If the region size is 0, nothing is selected
				# Instead run inversion across the whole view
				region = sublime.Region(0, self.view.size())

			text = self.view.substr(region).strip()
			replace_text = invert_json_string(text)
			self.view.replace(edit, region, replace_text)

def invert_json_string(text: str, indent: str = "\t") -> str:
	"""Either string encode or decode a `str` containing JSON"""
	if is_json_string(text):
		# Decode JSON string to raw JSON
		return json.loads(text)

	# Encode raw JSON to a JSON string
	# We pass this through loads->dumps->dumps to convert any indentation to '\t' characters. This
	# way, when the resultant string is inverted back Sublime Text correctly translates the '\t'
	# character into the user's current indentation setting.
	return json.dumps(json.dumps(json.loads(text), indent=indent))

def is_json_string(text: str) -> bool:
	"""
	Given an input text, is_json_string returns `True` if it is a valid JSON string, or False otherwise.

	The definition of a valid JSON string is set out in the JSON specification available at https://json.org/.
	Specifically, the section on strings defines them as: "A string is a sequence of zero or more
	Unicode characters, wrapped in double quotes, using backslash escapes."
	"""

	# Valid state machine states
	empty_state = "EMPTY"
	inside_string_state = "INSIDE_STRING"
	start_escape_state = "START_ESCAPE"
	end_string_state = "END_STRING"

	state = empty_state
	for char in text:
		if state == empty_state:
			# EMPTY state is the start of the JSON string, the current character must be a double-quote character: "
			if char == "\"":
				state = inside_string_state
			else:
				return False

		elif state == inside_string_state:
			# INSIDE_STRING state is any characters inside the body of the string.
			# The inside of a string can be any Unicode character other than \ and "
			# 	- \ signifies the begin of an escape sequence
			# 	- " signifies the end of the JSON string
			if char == "\\":
				state = start_escape_state
			elif char == "\"":
				state = end_string_state

		elif state == start_escape_state:
			# START_ESCAPE state is entered when a \ was the previous character. The next character
			# must be one of ", \, /, b, f, b, r, t, or u to define a valid escape sequence.
			if char in ["\"", "\\", "/", "b", "f", "n", "r", "t", "u"]:
				state = inside_string_state
			else:
				return False

		elif state == end_string_state:
			# END_STRING is entered if the previous character we parsed was the string closing
			# double-quote. If there are still more characters to process text is not a valid JSON string.
			return False

		else:
			# If we don't enter a valid state branch, somehow we've gotten into an invalid state and we cannot continue
			raise Exception("Invalid state machine state: {}".format(state))

	# If we managed to parse the entire string without error, we know we have a JSON string
	return True
