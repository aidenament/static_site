# Claude Code Reimplementation

[< Back to Projects](/projects)

## An Agentic Coding Assistant Built on Google Gemini

An agentic coding assistant written from scratch in about 380 lines of Python, with no agent framework. It gives the model four tools, listing a directory, reading a file, writing a file, and running a Python file, then lets it work on its own until it decides the task is done.

The goal was to understand the pattern by building it. Stripped of streaming, permissions, and subagents, an agent loop is a small thing: send the conversation, execute whatever tool calls come back, append the results, and send it again. Writing that by hand makes the design questions visible in a way that using a framework does not.

### GitHub Repository

View the source code: [github.com/aidenament/Claude-Code-Reimplementation](https://github.com/aidenament/Claude-Code-Reimplementation)

### The Agent Loop

Two nested loops. The outer one is a user turn; the inner one is the model working autonomously. Each model response is appended to the history, every tool call it contains is executed, and each result is appended as a tool message before the next request goes out.

Termination is inferred rather than declared. When a response comes back containing no tool calls, that is the signal that the model is finished: the loop prints its text and returns control to the user. This avoids inventing a dedicated "done" tool, at the cost that a model which is stuck looks exactly like a model which is finished.

The inner loop is bounded at twenty tool calls per turn. The bound is tested once per model request rather than once per call, so a response carrying several calls at once runs all of them and can finish slightly over the limit. On reaching it the loop reports that it stopped and returns to the prompt with the conversation history intact, so the work so far can be inspected and continued rather than discarded.

Responses carrying several tool calls at once are fully serviced, with a separate result appended for each, so the model can request a directory listing and two file reads in one turn and get all three answers back.

### Tool Design

The results are shaped for a reader that is a language model rather than a person.

**Errors are values, not exceptions.** Tools report their failures by returning a string rather than raising. A bad path comes back as an "Error: ..." string through the same channel as a successful result, so the model reads its own mistake and can correct course instead of the process terminating. The convention is not airtight: an unreadable directory still raises out of the listing, and because no schema marks its parameters required, a call that omits one fails inside the tool rather than returning a message the model could act on.

**Truncation is announced.** File reads are capped at 10,000 characters, and the notice is appended into the returned text rather than the content being silently cut short, so the model knows its view is partial.

**Empty output gets a sentinel.** A script that prints nothing returns an explicit "No output produced" rather than an empty string, and a nonzero exit adds a line stating the exit code. Standard output and standard error are labelled separately, so a silent run is distinguishable from a run that produced nothing to say.

**Writes confirm what happened.** A successful write returns the path and the number of characters written, which the model can check against what it intended.

**Listings degrade per entry.** Directory listings wrap the size and directory checks for each entry individually, so a single unreadable file becomes an inline error on that row instead of failing the whole listing.

### Tool Declarations and Dispatch

The four tool schemas are hand written declarations, kept separately from the functions implementing them. There is no reflection over the Python signatures, so the schema and the implementation are maintained in parallel by hand. Dispatch is an explicit match on the tool name, and an unrecognized name returns an error result rather than raising.

The working directory root is deliberately absent from every tool schema. The model can name a path but never its base; the dispatcher supplies the root itself, so the root cannot be redefined by the model.

Each tool then resolves the requested path and compares it against that root before acting. The comparison is a string prefix test, which is the loose form of the check: a strict version would compare the common path of the two resolved paths, which is what correctly rejects a sibling directory sharing a name prefix, and would resolve symbolic links rather than normalizing them lexically.

Execution runs the target file as a subprocess with the working directory as its starting point and a thirty second timeout, and only files ending in .py are eligible.

### Technologies Used

- **Python** with the Google Gen AI SDK
- **Gemini 2.5 Flash**, pinned to the `gemini-2.5-flash-preview-05-20` snapshot
- No web framework, database, or dependencies beyond the SDK and a dotenv loader
