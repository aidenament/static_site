# Claude Code Reimplementation

[< Back to Projects](/projects)

## An Agentic Coding Assistant Built on Google Gemini

An agentic coding assistant in about 380 lines of Python, with no agent framework. It gives the model four tools, listing a directory, reading a file, writing a file, and running a Python file, then lets it work until it decides the task is done.

I built it to understand the pattern. Strip out streaming, permissions and subagents and an agent loop is a small thing: send the conversation, run whatever tool calls come back, append the results, send it again. Writing that by hand puts the design questions in front of you.

### GitHub Repository

View the source code: [github.com/aidenament/Claude-Code-Reimplementation](https://github.com/aidenament/Claude-Code-Reimplementation)

### The Agent Loop

Two nested loops. The outer one is a user turn; the inner one is the model working on its own.

The loop never asks the model whether it's finished. When a response comes back with no tool calls in it, that's the signal: print the text and hand control back to the user. It saves inventing a "done" tool, and it costs you the ability to tell a model that's finished from a model that's stuck.

The inner loop stops at twenty tool calls. That bound gets tested once per model request, not once per call, so a response asking for a directory listing and two file reads runs all three and can finish slightly over. Hitting the limit isn't a failure. The loop says it stopped and returns to the prompt with the history intact, so you can look at what happened and tell it to keep going.

### Tool Design

Every tool result is written to be read by a model.

**Errors are values.** Tools report failures by returning a string. A bad path comes back as "Error: ..." through the same channel as a success, so the model sees its own mistake and can recover. It isn't airtight. An unreadable directory still raises, and since no schema marks its parameters required, a call that omits one dies inside the tool.

**Truncation is announced.** Reads stop at 10,000 characters and the notice goes into the returned text. Nothing gets cut silently.

**Empty output gets a sentinel.** A script that prints nothing returns "No output produced", and a nonzero exit adds a line with the exit code. Standard output and standard error are labelled separately.

**Writes confirm themselves.** A successful write returns the path and the character count, which the model can check against what it meant to write.

**Listings degrade per entry.** The size and directory checks are wrapped for each entry individually. One unreadable file becomes an error on that row and the rest of the listing survives.

### Declarations and Dispatch

The four schemas are hand written, and they live in a different file from the functions implementing them. Nothing reflects over the Python signatures. The two have to be kept in step by hand. Dispatch is an explicit match on the tool name.

The working directory root never appears in a tool schema. The model can name a path but not its base; the dispatcher supplies the root. The root isn't something the model can redefine.

Each tool then resolves the path it was given and compares it against that root. The check is a string prefix test, which is the loose version: a root of /work/project also accepts /work/project-old. The strict version compares the common path of the two resolved paths, and resolves symbolic links instead of normalising them lexically.

Execution runs the target as a subprocess with the working directory as its starting point and a thirty second timeout. Only files ending in .py are eligible.

### Technologies Used

- **Python** with the Google Gen AI SDK
- **Gemini 2.5 Flash**, pinned to the `gemini-2.5-flash-preview-05-20` snapshot
- No web framework, database, or dependencies beyond the SDK and a dotenv loader
