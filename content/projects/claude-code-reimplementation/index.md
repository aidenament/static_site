# Claude Code Reimplementation

[< Back to Projects](/projects)

## AI Agent Development Assistant

This project is an AI-powered development assistant designed to help users with Python development and file system operations within a secure, sandboxed environment. It's a reimplementation of Claude Code using the Gemini AI model.

### GitHub Repository

View the source code: [github.com/aidenament/Claude-Code-Reimplementation](https://github.com/aidenament/Claude-Code-Reimplementation)

### Overview

The AI Agent leverages the Gemini AI model to understand user prompts and execute various coding and file management tasks. It's equipped with specific tool functions that allow it to interact with the file system, read/write files, and run Python scripts, all while maintaining strict security boundaries to prevent unauthorized access.

### Key Features

- **Intelligent AI Interaction**: Utilizes the Gemini AI model to interpret natural language requests and determine appropriate actions
- **File System Exploration**: Capability to list files and directories to understand project structure
- **File Content Management**: Read and write content to files, facilitating code modification and documentation
- **Python Code Execution**: Run Python scripts within the sandboxed environment to test and verify code
- **Secure Operations**: All file system operations are constrained to the working directory, ensuring a secure and controlled environment
- **Interactive Mode**: Engage with the AI agent in a conversational manner for continuous development tasks
- **Command-Line Prompting**: Provide initial prompts directly via command-line arguments for specific tasks

### Technical Architecture

#### Core Components

**main.py**: The main script that orchestrates the AI agent, handling conversation flow, AI model interaction, and dispatching tool calls <br> <br>
**functions/**: Contains the implementations of the tool functions available to the AI agent:

 - **get_files_info.py**: Lists files and their metadata
 - **get_file_content.py**: Reads the content of specified files
 - **run_python.py**: Executes Python scripts
 - **write_file_content.py**: Writes content to files securely

#### Example Application

The repository includes a calculator application as an example that the AI agent can interact with:

- **calculator/main.py**: The main script for the calculator application
- **calculator/tests.py**: Unit tests for the calculator
- **calculator/pkg/**: Contains core logic for evaluating arithmetic expressions and formatting output

### Usage Examples

> **Interactive Mode** <br>
> python main.py

> **Command-Line Prompt** <br>
> python main.py "list all python files"

> **Verbose Mode** <br>
> python main.py --verbose

### Security Considerations

The assistant implements several security measures:
- File system operations are restricted to the working directory
- Python script execution is sandboxed
- All operations are logged and can be audited
- Environment variables are properly isolated

### Technologies Used

- **Python 3.x**
- **Google Gemini AI**
- **Secure file system operations**

