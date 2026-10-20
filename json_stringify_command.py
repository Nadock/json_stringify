"""
Implementation of json_stringify plugin for Sublime Text 3. It converts between JSON and JSON string representations of data.
"""
import collections
import json

# pylint: disable=import-error
# These modules are provided by SublimeText, so they are not going to be installed wherever the linting runs
import sublime
import sublime_plugin
# pylint: enable=import-error

def run_on_selections(view, edit, convert):
	"""
	Replace each selection in `view` with `convert` applied to its text, or the whole view when nothing is selected.

	Every replacement is worked out before the view is changed, so if any selection cannot be converted the status
	bar says why and the text is left as it was. Whitespace around a selection is kept. Replacements are applied from
	the end of the view to the start so an earlier one cannot move a later one.
	"""
	regions = [region for region in view.sel() if region.size() > 0]
	if not regions:
		regions = [sublime.Region(0, view.size())]

	replacements = []
	for region in regions:
		text = view.substr(region)
		core = text.strip()
		if not core:
			continue

		try:
			converted = convert(core)
		except ValueError as error:
			sublime.status_message("JSON Stringify: {}".format(error))
			return

		leading = text[:len(text) - len(text.lstrip())]
		trailing = text[len(text.rstrip()):]
		replacements.append((region, leading + converted + trailing))

	for region, replace_text in sorted(replacements, key=lambda item: item[0].begin(), reverse=True):
		view.replace(edit, region, replace_text)

class JsonStringifyCommand(sublime_plugin.TextCommand): # pylint: disable=too-few-public-methods
	"""
	The implementing class for the json_stringify ST3 plugin.

	Converts a selection either from some valid JSON data type to a JSON string or from a JSON
	string to the underlying data structure. The plugin runs on each selection of text in a
	view, or the entire text of the view when nothing is selected.
	"""
	def run(self, edit):
		"""Run the json_stringify plugin"""
		run_on_selections(self.view, edit, invert_json_string)

class JsonStringifyEncodeCommand(sublime_plugin.TextCommand): # pylint: disable=too-few-public-methods
	"""Always encode each selection (or the whole view) as a JSON string."""
	def run(self, edit):
		"""Run the json_stringify_encode command"""
		run_on_selections(self.view, edit, encode_json_string)

class JsonStringifyDecodeCommand(sublime_plugin.TextCommand): # pylint: disable=too-few-public-methods
	"""Always decode each selection (or the whole view) from a JSON string."""
	def run(self, edit):
		"""Run the json_stringify_decode command"""
		run_on_selections(self.view, edit, decode_json_string)

def invert_json_string(text: str, indent: str = "\t") -> str:
	"""Either string encode or decode a `str` containing JSON"""
	try:
		return decode_json_string(text)
	except ValueError:
		return encode_json_string(text, indent)

def decode_json_string(text: str) -> str:
	"""
	Decode a JSON string (a double quoted string with backslash escapes) to the text it holds.

	Raises a `ValueError` saying why if `text` is not a JSON string.
	"""
	value = json.loads(text)
	if not isinstance(value, str):
		raise ValueError("the text is not a JSON string")
	return value

def encode_json_string(text: str, indent: str = "\t") -> str:
	"""
	Encode `text` as a JSON string.

	If `text` is a JSON document it is first written out again with `indent` and the object keys in their original
	order. This way, when the resultant string is decoded Sublime Text correctly translates the '\t' character into the
	user's current indentation setting. Any other text is encoded as it is. Characters outside ASCII are kept, not
	turned into \\u escapes.
	"""
	try:
		document = json.loads(text, object_pairs_hook=collections.OrderedDict)
	except ValueError:
		return json.dumps(text, ensure_ascii=False)

	return json.dumps(json.dumps(document, indent=indent, separators=(",", ": "), ensure_ascii=False), ensure_ascii=False)

def is_json_string(text: str) -> bool:
	"""Given an input text, is_json_string returns `True` if it is a valid JSON string, or False otherwise."""
	try:
		decode_json_string(text)
	except ValueError:
		return False
	return True
