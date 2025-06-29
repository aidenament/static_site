# Story Teller AI 🐘

[< Back to Projects](/projects)

## An Interactive AI-Powered Storytelling Application

Story Teller is an interactive AI-powered storytelling application featuring Boop Boop the Storytelling Elephant, designed to create and narrate engaging stories for children aged 5-10 years old. Originally developed as an interview project for Hippocratic AI.

### GitHub Repository

View the source code: [github.com/aidenament/Story-Teller-AI](https://github.com/aidenament/Story-Teller-AI)

### Overview

Story Teller is a multi-agent AI system that creates personalized, age-appropriate stories through an interactive conversation with children. The application uses a sophisticated orchestration of AI agents to generate, refine, and narrate stories that capture children's imagination while teaching valuable lessons.

### System Architecture

![Story Teller Architecture Diagram](/images/Diagram.png)

### Key Features

- **Interactive Story Creation**: Children can request specific story ideas or let Boop Boop suggest one
- **Multi-Agent System**: 
  - **Story Selection Agent**: Warmly interacts with children to understand their story preferences
  - **Secret Story Judge**: Works behind the scenes to enhance story outlines with rich details
  - **Story Telling Agent**: Brings stories to life with vivid narration and engaging language
- **Age-Appropriate Content**: Stories are carefully crafted for 5-10 year olds with simple yet rich language
- **Engaging Narration**: Uses sound effects, vivid descriptions, and pacing to keep children engaged
- **Educational Value**: Each story includes a moral or lesson naturally woven into the narrative

### How It Works

1. **Story Selection**: Boop Boop interacts with the child to understand their story preferences
2. **Outline Creation**: Based on the child's input, a detailed story outline is created
3. **Outline Enhancement**: The Secret Story Judge silently improves the outline with rich details
4. **Story Narration**: Boop Boop reads the enhanced outline and narrates a complete, engaging story
5. **Paced Delivery**: The story is delivered in paragraphs with natural pacing for better engagement

### Technical Implementation

The project demonstrates several advanced AI concepts:

- **Multi-Agent Orchestration**: Different AI agents handle specific aspects of the storytelling process
- **Context Management**: Maintains conversation context across agent handoffs
- **Prompt Engineering**: Carefully crafted prompts ensure age-appropriate and engaging content
- **Tool Integration**: Uses file system operations for persistent story management

### Model Considerations

The default model for this project is GPT-3.5-turbo as the company requested. This impacted design considerations for:
- Tool usage and handoffs are carefully managed due to model limitations
- The system includes additional guidance and reminders to prevent errors
- Significant improvements are observed when using more capable models like GPT-4.1. I highly recommend using with this model if possible

### Usage Example

> python main.py

The application will:

1. Introduce Boop Boop the Storytelling Elephant
2. Ask if you have a specific story idea or would like a suggestion
3. Create a story outline based on your preferences
4. Narrate the complete story with engaging details and pacing

### Technologies Used

- **Python 3.7+**
- **OpenAI API**
- **Weights and Biases (for tracking and debugging)**
