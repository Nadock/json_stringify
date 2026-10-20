# JSON Stringify
A SublimeText 3 plugin to encode and decode JSON strings.

![JSON Stringify in action](https://thumbs.gfycat.com/GracefulMintyHoiho-size_restricted.gif)

## Installation
This plugin can be installed with [PackageControl](https://packagecontrol.io/packages/JSON%20Stringify).

## Usage Instructions
1. Open the Command Palette with `Cmd + Shift + P` (MacOS) or `Ctrl + Shift + P` (Linux/Windows)
2. Search for one of these commands and press `Enter`:
	- `JSON Stringify: Invert Selection` decodes the selection if it is a JSON string, otherwise encodes it as one.
	- `JSON Stringify: Encode Selection` always encodes the selection as a JSON string.
	- `JSON Stringify: Decode Selection` always decodes the selection from a JSON string.

Each command works on every selection, or on the whole file when nothing is selected. If a selection cannot be converted, the status bar says why and nothing is changed.
