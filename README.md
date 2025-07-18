# 🤖 Build with AI — Simple Q\&A Application

This project demonstrates how to build a simple Question & Answer application powered by Google Gemini models using the **LangChain** framework and other powerful Python tools for natural language processing, document handling, and vector search.

---

## 🛠️ Tools & Libraries Used

| Library                    | Purpose                                               |
| -------------------------- | ----------------------------------------------------- |
| `python-dotenv`            | Manage environment variables from a `.env` file       |
| `langchain`                | Framework for building LLM-powered applications       |
| `langchain-community`      | Community-contributed integrations for LangChain      |
| `langchain-google-genai`   | Integration with Google Gemini models                 |
| `google-generativeai`      | Direct access to Google Gemini API                    |
| `unstructured`             | Load and preprocess documents                         |
| `nltk`                     | Text processing and tokenization                      |
| `chromadb`                 | Vector database for storing and retrieving embeddings |
            

---

## 🚀 Getting Started

### 1. Fork the Repository

Click the **Fork** button at the top right to clone this repository into your GitHub account.

### 2. Clone and Set Up

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 3. Install Requirements

Use `pip` to install all required packages:

```bash
pip install -r requirements.txt
```

> 💡 **Note for macOS users**:
> If installing `chromadb` fails, try using `conda`:
>
> ```bash
> conda install onnxruntime -c conda-forge
> ```

> ⚠️ **Note for Windows users**:
> You may need to install the **Microsoft Visual C++ Build Tools** before installing `onnxruntime`.

---

## 🔑 Set Your Gemini API Key

### 1. Get Your API Key

Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to generate your Gemini API key.

### 2. Set the API Key in Your Environment

#### macOS / Linux:

```bash
export GEMINI_API_KEY="your-actual-api-key"
python main.py
```

#### Windows (Command Prompt):

```cmd
set GEMINI_API_KEY=your-actual-api-key
python main.py
```

> 💡 Alternatively, create a `.env` file in the project root:
>
> ```
> GEMINI_API_KEY=your-actual-api-key
> ```

---

## 📦 Running the Application

Once everything is set up, simply run:

```bash
python main.py
```

The app will process your input and respond using the Gemini model.



