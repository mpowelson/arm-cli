import os
import json
import requests
from pathlib import Path
from typing import List, Optional, Dict, Any
import click

from arm_cli.settings import get_setting, set_setting, get_settings_dir


class ChatbotRAG:
    """Lightweight RAG chatbot using Sentence Transformers and ChromaDB."""
    
    def __init__(self):
        self.settings_dir = get_settings_dir()
        self.data_dir = self.settings_dir / "chatbot"
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.embedding_model = None
        self.vector_db = None
        self.collection = None
        self.documents = []
        
    def _check_dependencies(self) -> bool:
        """Check if required dependencies are installed."""
        try:
            import sentence_transformers
            import chromadb
            return True
        except ImportError:
            return False
    
    def _install_dependencies(self):
        """Install required dependencies."""
        click.echo("Installing required dependencies...")
        os.system("pip install sentence-transformers chromadb")
        click.echo("Dependencies installed successfully!")
    
    def initialize(self):
        """Initialize the chatbot components."""
        if not self._check_dependencies():
            click.echo("Required dependencies not found. Installing...")
            self._install_dependencies()
        
        try:
            from sentence_transformers import SentenceTransformer
            import chromadb
            
            # Initialize embedding model (lightweight, CPU-friendly)
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Initialize ChromaDB
            self.vector_db = chromadb.PersistentClient(
                path=str(self.data_dir / "chroma_db")
            )
            
            # Create or get collection
            try:
                self.collection = self.vector_db.get_collection("arm_cli_docs")
            except:
                self.collection = self.vector_db.create_collection("arm_cli_docs")
            
            click.echo("Chatbot initialized successfully!")
            return True
            
        except Exception as e:
            click.echo(f"Failed to initialize chatbot: {e}")
            return False
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Add documents to the knowledge base."""
        if not self.collection:
            click.echo("Chatbot not initialized. Run 'arm-cli guide chatbot enable' first.")
            return
        
        try:
            # Prepare documents for ChromaDB
            texts = [doc.get('content', '') for doc in documents]
            metadatas = [doc.get('metadata', {}) for doc in documents]
            ids = [f"doc_{i}" for i in range(len(documents))]
            
            # Add to collection
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            click.echo(f"Added {len(documents)} documents to knowledge base.")
            
        except Exception as e:
            click.echo(f"Failed to add documents: {e}")
    
    def query(self, question: str, top_k: int = 3) -> str:
        """Query the knowledge base and return a response."""
        if not self.collection:
            return "Chatbot not initialized. Run 'arm-cli guide chatbot enable' first."
        
        try:
            # Search for relevant documents
            results = self.collection.query(
                query_texts=[question],
                n_results=top_k
            )
            
            if not results['documents'] or not results['documents'][0]:
                return "I don't have enough information to answer that question. Try adding some documentation first."
            
            # Simple response generation (can be enhanced later)
            relevant_docs = results['documents'][0]
            response = f"Based on the documentation, here's what I found:\n\n"
            
            for i, doc in enumerate(relevant_docs, 1):
                response += f"{i}. {doc[:200]}...\n\n"
            
            return response
            
        except Exception as e:
            return f"Error querying knowledge base: {e}"
    
    def load_local_docs(self, docs_path: str):
        """Load documentation from a local file."""
        try:
            docs_file = Path(docs_path)
            if not docs_file.exists():
                click.echo(f"Documentation file not found: {docs_path}")
                return
            
            # Support different formats
            if docs_file.suffix == '.json':
                with open(docs_file, 'r') as f:
                    docs = json.load(f)
            elif docs_file.suffix == '.txt':
                with open(docs_file, 'r') as f:
                    content = f.read()
                    docs = [{'content': content, 'metadata': {'source': str(docs_file)}}]
            else:
                click.echo(f"Unsupported file format: {docs_file.suffix}")
                return
            
            self.add_documents(docs)
            
        except Exception as e:
            click.echo(f"Failed to load local docs: {e}")
    
    def fetch_remote_docs(self, url: str):
        """Fetch documentation from a remote URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Try to parse as JSON first
            try:
                data = response.json()
                # Handle different JSON structures
                if isinstance(data, list):
                    docs = data
                elif isinstance(data, dict):
                    # Convert dict to list format
                    docs = [{'content': str(data), 'metadata': {'source': url}}]
                else:
                    docs = [{'content': str(data), 'metadata': {'source': url}}]
            except:
                # Treat as plain text
                docs = [{'content': response.text, 'metadata': {'source': url}}]
            
            self.add_documents(docs)
            click.echo(f"Successfully fetched documentation from {url}")
            
        except Exception as e:
            click.echo(f"Failed to fetch remote docs: {e}")


# Global chatbot instance
_chatbot = None


def get_chatbot() -> ChatbotRAG:
    """Get or create the global chatbot instance."""
    global _chatbot
    if _chatbot is None:
        _chatbot = ChatbotRAG()
    return _chatbot


@click.group()
def chatbot():
    """Access ARM CLI chatbot with RAG capabilities."""
    pass


@chatbot.command()
@click.option('--question', '-q', help='Question to ask the chatbot')
@click.option('--docs', '-d', help='Path to local documentation file')
@click.option('--remote', '-r', help='URL to fetch remote documentation')
def chat(question: Optional[str], docs: Optional[str], remote: Optional[str]):
    """Start a chat session with the chatbot."""
    if not get_setting('chatbot_enabled'):
        click.echo("Chatbot is disabled. Enable it with 'arm-cli guide chatbot enable'")
        return
    
    bot = get_chatbot()
    
    # Initialize if needed
    if not bot.collection:
        if not bot.initialize():
            return
    
    # Load documentation if provided
    if docs:
        bot.load_local_docs(docs)
    
    if remote:
        bot.fetch_remote_docs(remote)
    
    # Interactive mode or single question
    if question:
        response = bot.query(question)
        click.echo(response)
    else:
        click.echo("ARM CLI Chatbot (type 'quit' to exit)")
        click.echo("=" * 50)
        
        while True:
            try:
                user_input = click.prompt("You", prompt_suffix=": ")
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                response = bot.query(user_input)
                click.echo(f"\nBot: {response}\n")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                click.echo(f"Error: {e}")


@chatbot.command()
def enable():
    """Enable the chatbot feature."""
    set_setting('chatbot_enabled', True)
    click.echo("Chatbot enabled! Run 'arm-cli guide chatbot chat' to start chatting.")


@chatbot.command()
def disable():
    """Disable the chatbot feature."""
    set_setting('chatbot_enabled', False)
    click.echo("Chatbot disabled.")


@chatbot.command()
def status():
    """Show chatbot status and information."""
    enabled = get_setting('chatbot_enabled')
    click.echo(f"Chatbot enabled: {enabled}")
    
    if enabled:
        bot = get_chatbot()
        if bot.collection:
            click.echo("Status: Initialized and ready")
            # Get collection info
            try:
                count = bot.collection.count()
                click.echo(f"Documents in knowledge base: {count}")
            except:
                click.echo("Documents in knowledge base: 0")
        else:
            click.echo("Status: Not initialized (run 'arm-cli guide chatbot chat' to initialize)")
    else:
        click.echo("Status: Disabled")