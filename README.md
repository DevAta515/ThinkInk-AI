
```markdown
# ThinkInk-AI Blog Generator API

A sophisticated AI-powered blog generation system that creates SEO-optimized blog content and provides multi-language translation capabilities using LangGraph workflow orchestration.

## 🚀 Overview

ThinkInk-AI is a FastAPI-based application that leverages Large Language Models (LLMs) through LangGraph to automatically generate blog content from topics and provide translations in multiple languages. The system uses a structured workflow to ensure high-quality, formatted content generation.

## 🏗️ Architecture

### Core Components

#### 1. **State Management**
- **BlogState**: Pydantic model managing the blog generation workflow state
- Tracks: topic, title, content, current language, and translations

#### 2. **Graph Workflow**
- **LangGraph StateGraph**: Orchestrates the blog generation pipeline
- **Dynamic Routing**: Conditionally routes to translation based on language requirements
- **Modular Nodes**: Each node handles a specific aspect of content creation

#### 3. **LLM Integration**
- **GroqLLM**: High-performance LLM provider for fast inference
- **Structured Output**: Ensures consistent blog format and structure

### Workflow Pipeline

```
START → Title Creation → Content Generation → Language Router → [Translation] → END
```

## 🛠️ Technology Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs with Python 3.7+
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation and settings management using Python type annotations

### AI/ML Stack
- **LangGraph**: Framework for building stateful, multi-actor applications with LLMs
- **GroqLLM**: High-speed LLM inference engine
- **LangChain**: Framework for developing applications powered by language models

### Development & Deployment
- **Python 3.9+**: Core programming language
- **LangSmith**: Monitoring and debugging for LLM applications
- **WatchFiles**: Auto-reload during development

## 📋 API Endpoints

### 1. Health Check
**GET** `/health`

Verifies that the API is running and checks component status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "service": "ThinkInk-AI Blog Generator",
  "version": "1.0.0"
}
```

### 2. Generate Blog
**POST** `/generate-blog/`

Generates a complete blog post with optional translation.

**Request Body:**
```json
{
  "topic": "Artificial Intelligence in Healthcare",
  "language": "spanish"  // Optional: specifies translation language
}
```

**Response:**
```json
{
  "blog": {
    "title": "The Transformative Role of AI in Modern Healthcare",
    "content": "# The Transformative Role of AI in Modern Healthcare...",
    "language": "spanish"
  },
  "status": "success"
}
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- Groq API key
- Git

### Step-by-Step Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/ThinkInk-AI.git
   cd ThinkInk-AI
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   LANGCHAIN_API_KEY=your_langsmith_key_here  # Optional
   LANGCHAIN_TRACING_V2=true  # Optional for LangSmith monitoring
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```
   or with auto-reload:
   ```bash
   python app.py --reload
   ```

6. **Access the API**
   - API: http://localhost:8080
   - Interactive Documentation: http://localhost:8080/docs
   - Alternative Documentation: http://localhost:8080/redoc

## 🎯 Usage Examples

### Basic Blog Generation
```python
import requests

payload = {
    "topic": "Machine Learning Trends 2024"
}

response = requests.post("http://localhost:8080/generate-blog/", json=payload)
print(response.json())
```

### Multi-language Blog Generation
```python
payload = {
    "topic": "Sustainable Energy Solutions",
    "language": "french"  # Supports any language
}

response = requests.post("http://localhost:8080/generate-blog/", json=payload)
```

### Using cURL
```bash
# Health check
curl http://localhost:8080/health

# Generate blog
curl -X POST "http://localhost:8080/generate-blog/" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Climate Change Solutions", "language": "german"}'
```

### Available Languages
The system supports dynamic translation for any language, including:
- Spanish, French, German, Hindi, Japanese, Chinese, Arabic, and more

## 🔍 Graph Architecture Details

### Node Functions

1. **Title Creation Node**
   - Generates SEO-optimized, creative blog titles
   - Uses markdown formatting
   - Ensures topic relevance

2. **Content Generation Node**
   - Creates detailed, structured blog content
   - Uses markdown for formatting
   - Provides comprehensive topic coverage

3. **Language Router Node**
   - Determines if translation is needed
   - Routes to appropriate translation path
   - Handles conditional workflow logic

4. **Dynamic Translation Node**
   - Translates content to any specified language
   - Maintains original tone and formatting
   - Adapts cultural references appropriately

### State Transitions
```python
BlogState = {
    "topic": str,
    "blog": {
        "title": str,
        "content": str
    },
    "curr_lang": str,  # Current target language
}
```

## 🚀 Performance Features

- **Fast Inference**: GroqLLM provides high-speed model inference
- **Concurrent Processing**: Async/await support for high throughput
- **Memory Efficient**: Optimized state management
- **Scalable Architecture**: Modular design for easy extensions

## 🔒 Error Handling

The system includes comprehensive error handling:
- LLM API failure fallbacks
- Structured output validation
- Graceful degradation for translation failures
- Detailed logging for debugging

## 📊 Monitoring & Debugging

### LangSmith Integration (Optional)
- Trace all LLM calls
- Monitor performance metrics
- Debug workflow execution
- Analyze token usage

### Logging
- Detailed execution logs
- Error tracking and reporting
- Performance monitoring

## 🗂️ Project Structure

```
ThinkInk-AI/
├── src/
│   ├── graphs/
│   │   └── graphbuilder.py      # LangGraph workflow definition
│   ├── llms/
│   │   └── groqllm.py          # LLM configuration and setup
│   ├── nodes/
│   │   └── blog_node.py        # Blog generation nodes
│   └── states/
│       └── blog_state.py       # Pydantic state models
├── app.py                      # FastAPI application
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🆘 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find and kill process using port 8080
   netstat -ano | findstr :8080
   taskkill /PID <PID> /F
   ```

2. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. **API Key Issues**
   - Verify GROQ_API_KEY in .env file
   - Check API quota and limits

4. **LangSmith Connection**
   - Optional component - API works without it
   - Set LANGCHAIN_TRACING_V2=false to disable

### Getting Help

- Check API documentation at `/docs`
- Review application logs
- Verify environment variables
- Test with simple topics first

## 🔮 Future Enhancements

- [ ] Support for multiple blog formats
- [ ] Image generation integration
- [ ] SEO optimization suggestions
- [ ] Multi-language simultaneous translation
- [ ] Custom tone and style settings
- [ ] Batch processing capabilities

---

**ThinkInk-AI** - Transforming ideas into well-crafted content, one topic at a time.

## 📞 Support

For support and questions:
1. Check the interactive API documentation at `/docs`
2. Review the application logs for detailed error information
3. Ensure all environment variables are properly configured

---
*Built with ❤️ using FastAPI, LangGraph, and GroqLLM*
```