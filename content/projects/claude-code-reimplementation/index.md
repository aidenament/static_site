# Claude Code Reimplementation

[< Back to Projects](/projects)

## A From-Scratch Study of the Agent Loop

An agentic coding assistant built on Google Gemini, in about 380 lines of Python with no framework. It gives the model four tools, lists a directory, reads a file, writes a file, and runs a Python file, then lets it work autonomously until it decides it is finished.

The point was to understand the pattern rather than to ship a product. Stripped of streaming, permissions, and subagents, an agent loop is a small thing: send the conversation, execute whatever tools come back, append the results, and send it again. Writing that by hand makes the design questions visible in a way that using a framework does not.

### GitHub Repository

View the source code: [github.com/aidenament/Claude-Code-Reimplementation](https://github.com/aidenament/Claude-Code-Reimplementation)

### How the Loop Works

Two nested loops. The outer one is a user turn; the inner one is the model working on its own. Each model response is appended to the history, every tool call in it is executed, and each result is appended as a tool message. When a response comes back with no tool calls at all, that is the termination signal: the loop prints the text and hands control back to the user.

Inferring termination from an empty tool call list is the simplest thing that works, and it has one real consequence worth naming. The model cannot distinguish "I am finished" from "I am stuck," because both look identical from outside.

A few details in the tool layer are worth calling out, because they are the parts that separate an agent loop that works from one that quietly confuses the model:

- **Errors are values, not exceptions.** Every tool returns a string, including its failures. A bad path comes back as "Error: ..." in the same channel as a successful result, so the model reads its own mistake and can correct it instead of the process dying.
- **Truncation is announced.** Reads are capped at 10,000 characters, and the notice is appended into the returned text rather than the file being silently cut short. The model is told its read was incomplete.
- **Empty output gets a sentinel.** A script that prints nothing returns "No output produced" rather than an empty string, and a nonzero exit adds an explicit line saying so. Handing a model a blank tool result is a common way to confuse it.
- **Parallel calls are handled.** The loop iterates over every tool call in a response and appends a separate result for each, so a model that requests three at once gets three answers. Naive implementations tend to service only the first.
- **The call budget is a checkpoint, not a failure.** Twenty tool calls per turn, and on exhaustion it says so and returns to the prompt with the conversation intact, so the work can be inspected and resumed rather than lost.

The tool schemas are four hand-written declarations, kept in a different file from the functions that implement them. There is no reflection over the Python signatures, which means the schema and the implementation have to be maintained in parallel by hand.

### The Containment Boundary

The one design decision I would defend without reservation is that the working directory root is never part of any tool's schema. The model can name a path but never its base; the dispatcher supplies the root itself. That is the right shape, because it means the agent cannot widen its own scope through an argument, which is the failure mode that matters.

The enforcement underneath it is weaker than the design. Each tool resolves the requested path and compares it to the root with a string prefix test. A prefix test on a path is not containment, and it fails in at least three ways: a sibling directory whose name merely starts with the root's name passes it, since the resolved root carries no trailing separator; a symlink inside the root passes it, because resolving a path lexically does not follow links; and the check does not survive a root-relative path. The correct primitive is a real containment check, comparing the common path of the two resolved paths rather than comparing them as strings.

The repository's own smoke script probes this boundary rather than the happy path, and it catches the case it tests. It just never tested a sibling directory or a symlink, which is exactly why those survived.

Execution is likewise bounded in scope but not isolated. A subprocess is launched with the working directory as its starting point and a thirty second timeout. A starting directory is not a jail: the child runs as the same user, inherits the full environment, and keeps its network. The three real limits are that the script file must live under the root, must end in .py, and must finish inside the timeout.

### What It Is Not

Worth being direct, since the name invites the comparison. This is four tools and a while loop. There is no shell tool, no search, no diff-based editing (writes replace a whole file), no permission prompts, no subagents, no context compaction, and no streaming. There is also no retry around the API call, and the conversation lives only in memory, so a rate limit or a dropped connection ends the session and takes the history with it. Calling it a study of the agent loop is accurate; calling it a functional replacement for the tool it is named after is not.

### Stack

Python with the Google Gen AI SDK, targeting Gemini 2.5 Flash. No web framework, no database, no dependencies beyond the SDK and a dotenv loader. Roughly 380 lines for the agent, plus a small calculator application used as something for the agent to work on.
