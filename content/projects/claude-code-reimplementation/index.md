# Claude Code Reimplementation

[< Back to Projects](/projects)

## Building an Agent Loop From Scratch on Google Gemini

A small coding agent: four tools, one loop, about 380 lines of Python. It lists a directory, reads a file, writes a file and runs a Python file, and it keeps working on its own until it decides it's done.

### GitHub Repository

View the source code: [github.com/aidenament/Claude-Code-Reimplementation](https://github.com/aidenament/Claude-Code-Reimplementation)

### The Loop

Two nested loops. The outer one is a user turn, the inner one is the model working on its own.

The loop never asks the model whether it's finished. A response with no tool calls in it is the signal: print the text, hand control back. That saves inventing a "done" tool, and it costs you the ability to tell a finished model from a stuck one.

The inner loop stops at twenty tool calls, tested once per model request instead of once per call, so a response asking for three things at once runs all three and can land slightly over. Hitting the limit isn't a crash. The loop says it stopped and returns to the prompt with the history intact.

### Writing for a Model

Tools report failures by returning a string. A bad path comes back as "Error: ..." on the same channel as a success, so the model sees its own mistake and recovers instead of the process dying. It isn't airtight: an unreadable directory still raises, and no schema marks its parameters required, so a call that omits one dies inside the tool.

Reads stop at 10,000 characters and say so in the text they return. A script that prints nothing gets back "No output produced" instead of an empty string, and a nonzero exit adds a line with the code. Writes return a character count the model can check against what it meant to write. Directory listings wrap each entry's checks separately, so one unreadable file becomes an error on that row and the rest of the listing survives.

### Containment

The working directory root never appears in a tool schema. The model can name a path but not its base; the dispatcher supplies the root, so it isn't something the model can redefine.

Each tool then resolves the path it was given and compares it to that root with a string prefix test, which is the loose version: a root of /work/project also accepts /work/project-old. The strict version compares the common path of the two resolved paths and follows symlinks instead of normalising them lexically. Execution runs the target as a subprocess with a thirty second timeout, and only .py files are eligible.

### Technologies Used

- **Python** with the Google Gen AI SDK
- **Gemini 2.5 Flash**, pinned to the `gemini-2.5-flash-preview-05-20` snapshot
- No web framework, database, or dependencies beyond the SDK and a dotenv loader
