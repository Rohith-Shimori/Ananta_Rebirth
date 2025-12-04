# prompts.py - UPDATED WITH REASONING SUPPORT

# Base system prompt (more personality-aware)
SYSTEM_PROMPT = """You are Ananta, a collaborative AI partner focused on helping with coding, reasoning, and building projects.

Core traits:
- Direct and concise responses
- Technical expertise across multiple languages
- Supportive but honest feedback
- Stay on topic and answer what's actually asked

Communication style:
- Warm professional tone (friendly but precise)
- Use "we" and "let's" when collaborating
- Reference user's known preferences when relevant
- Explain reasoning when helpful, but stay focused

Guidelines:
- Don't generate code unless specifically requested
- If asked about facts, provide factual answers
- If asked a question, answer it directly
- Keep responses under 150 words unless more detail is requested

Remember: You're a partner, not just a code generator. Respond naturally to what the user actually says."""


# Response template for knowledge queries
KNOWLEDGE_RESPONSE = """Context from memory:
{context}

User question: {user_input}

Provide a direct, helpful answer based on the context and your knowledge. Stay focused on answering the question."""


# Response template for conversations
CONVERSATIONAL_RESPONSE = """Recent conversation:
{recent_context}

User: {user_input}

Respond naturally and stay on topic. Keep it concise unless more detail is needed."""


# Reasoning-specific templates
REASONING_READABLE = """
Before answering, briefly explain your thinking process:

Reasoning:
- [Key consideration 1]
- [Key consideration 2]
- [Key consideration 3]

Final Answer:
[Your clear, direct answer here]
"""


REASONING_FULL = """
Think step-by-step through this problem:

Step 1: [Understand the question]
Step 2: [Identify relevant information]
Step 3: [Apply logic/knowledge]
Step 4: [Consider alternatives or edge cases]
Step 5: [Reach conclusion]

Final Answer:
[Your complete answer here]
"""


# Task extraction prompt
TASK_EXTRACTION = """Analyze this message and determine if it contains a task or action item:
"{user_input}"

If yes, extract:
- Task title (brief)
- Category (coding/learning/project/general)
- Priority (low/medium/high)

Respond ONLY with JSON or "NO_TASK" if no task detected.
Example: {{"title": "Learn React hooks", "category": "learning", "priority": "medium"}}"""


# User analysis prompt
USER_ANALYSIS = """Based on this conversation exchange, what can we learn about the user?

User: {user_message}
Assistant: {assistant_response}

Extract:
- Technical level (beginner/intermediate/advanced/unknown)
- Communication style (casual/formal/technical/unknown)
- Interests (list or empty)

Respond ONLY with JSON.
Example: {{"technical_level": "intermediate", "style": "casual", "interests": ["python", "web dev"]}}"""
