"""
Vector Memory System using FAISS
"""
import faiss
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import pickle
import json


class VectorMemory:
    """
    Long-term memory using vector embeddings
    Supports storage and semantic search of knowledge chunks
    """
    
    def __init__(self, embedding_dim: int = 384, index_type: str = "flat"):
        self.embedding_dim = embedding_dim
        self.index_type = index_type
        self.index = None
        self.metadata_store = []
        self._initialize_index()
    
    def _initialize_index(self):
        """Initialize FAISS index"""
        if self.index_type == "flat":
            self.index = faiss.IndexFlatL2(self.embedding_dim)
        elif self.index_type == "ivf":
            # IVF index for larger datasets
            nlist = 100
            quantizer = faiss.IndexFlatL2(self.embedding_dim)
            self.index = faiss.IndexIVFFlat(quantizer, self.embedding_dim, nlist)
        else:
            self.index = faiss.IndexFlatL2(self.embedding_dim)
    
    def add(self, embeddings: np.ndarray, metadata: List[Dict]):
        """
        Add embeddings to memory with associated metadata
        
        Args:
            embeddings: numpy array of shape (n, embedding_dim)
            metadata: list of metadata dicts for each embedding
        """
        if len(embeddings) != len(metadata):
            raise ValueError("Embeddings and metadata must have same length")
        
        # Ensure embeddings are float32
        embeddings = embeddings.astype('float32')
        
        # Add to index
        self.index.add(embeddings)
        
        # Store metadata
        self.metadata_store.extend(metadata)
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Search for similar items in memory
        
        Args:
            query_embedding: query vector
            k: number of results to return
            
        Returns:
            List of (metadata, distance) tuples
        """
        if self.index.ntotal == 0:
            return []
        
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        
        # Search
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata_store):
                results.append((self.metadata_store[idx], float(dist)))
        
        return results
    
    def save(self, path: str):
        """Save memory to disk"""
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, str(path / "index.faiss"))
        
        # Save metadata
        with open(path / "metadata.pkl", 'wb') as f:
            pickle.dump(self.metadata_store, f)
        
        # Save config
        config = {
            'embedding_dim': self.embedding_dim,
            'index_type': self.index_type
        }
        with open(path / "config.json", 'w') as f:
            json.dump(config, f)
    
    def load(self, path: str):
        """Load memory from disk"""
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Memory not found at {path}")
        
        # Load config
        with open(path / "config.json", 'r') as f:
            config = json.load(f)
        
        self.embedding_dim = config['embedding_dim']
        self.index_type = config['index_type']
        
        # Load FAISS index
        self.index = faiss.read_index(str(path / "index.faiss"))
        
        # Load metadata
        with open(path / "metadata.pkl", 'rb') as f:
            self.metadata_store = pickle.load(f)
    
    def clear(self):
        """Clear all memory"""
        self._initialize_index()
        self.metadata_store = []
    
    @property
    def size(self) -> int:
        """Return number of items in memory"""
        return self.index.ntotal


class UserMemory:
    """
    User-specific memory tracking:
    - Knowledge level
    - Weak topics
    - Learning history
    - Progress
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.knowledge_level = {}  # topic -> level (0-1)
        self.weak_topics = []  # list of topics needing review
        self.learning_history = []  # list of learning sessions
        self.mistakes = {}  # question_id -> mistake_count
    
    def update_knowledge(self, topic: str, score: float, weight: float = 0.3):
        """
        Update knowledge level for a topic
        
        Args:
            topic: topic name
            score: performance score (0-1)
            weight: how much to weight this update
        """
        current = self.knowledge_level.get(topic, 0.5)
        self.knowledge_level[topic] = current * (1 - weight) + score * weight
        
        # Track weak topics
        if self.knowledge_level[topic] < 0.6:
            if topic not in self.weak_topics:
                self.weak_topics.append(topic)
        else:
            if topic in self.weak_topics:
                self.weak_topics.remove(topic)
    
    def record_mistake(self, question_id: str, topic: str = None):
        """Record a mistake on a question"""
        self.mistakes[question_id] = self.mistakes.get(question_id, 0) + 1
        
        # If topic provided, update knowledge level
        if topic:
            self.update_knowledge(topic, 0.3, weight=0.5)
    
    def record_session(self, session_data: Dict):
        """Record a learning session"""
        self.learning_history.append({
            'timestamp': session_data.get('timestamp', ''),
            'topics': session_data.get('topics', []),
            'score': session_data.get('score', 0),
            'duration': session_data.get('duration', 0)
        })
    
    def get_recommendations(self) -> List[str]:
        """Get recommended topics to study based on weak areas"""
        # Sort weak topics by mistake frequency
        topic_mistakes = {}
        for qid, count in self.mistakes.items():
            # Would need topic mapping in real implementation
            pass
        
        return self.weak_topics[:10]  # Return top 10 weak topics
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'user_id': self.user_id,
            'knowledge_level': self.knowledge_level,
            'weak_topics': self.weak_topics,
            'learning_history': self.learning_history[-100:],  # Last 100 sessions
            'mistakes': self.mistakes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserMemory':
        """Create from dictionary"""
        instance = cls(data['user_id'])
        instance.knowledge_level = data.get('knowledge_level', {})
        instance.weak_topics = data.get('weak_topics', [])
        instance.learning_history = data.get('learning_history', [])
        instance.mistakes = data.get('mistakes', {})
        return instance
