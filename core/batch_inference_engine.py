"""
Phase 5: Batch Inference Engine - Claude's Optimization Plan
Process multiple queries efficiently
- Batch similar queries together
- Use smallest sufficient model
- Maximize GPU utilization
"""

import asyncio
from typing import List, Dict, Optional, TYPE_CHECKING
import config

if TYPE_CHECKING:
    from core.ollama_client import OllamaClient

from dataclasses import dataclass
from enum import Enum
import config


class QueryComplexity(Enum):
    """Query complexity levels"""
    SIMPLE = 1      # 0-3 complexity
    MEDIUM = 2      # 3-7 complexity
    COMPLEX = 3     # 7-10 complexity


@dataclass
class BatchQuery:
    """Represents a query in a batch"""
    id: str
    query: str
    complexity: float
    model: str
    priority: int = 5
    status: str = "pending"  # pending, processing, completed
    result: Optional[str] = None


class QueryComplexityAnalyzer:
    """Analyzes query complexity for batching"""
    
    @staticmethod
    def analyze(query: str) -> float:
        """Estimate query complexity (0-10)"""
        words = len(query.split())
        
        # Base complexity from length
        complexity = min(words / 20.0, 3.0)
        
        # Keywords that increase complexity
        complex_keywords = ["prove", "derive", "algorithm", "architecture", "design"]
        for kw in complex_keywords:
            if kw in query.lower():
                complexity += 2.0
        
        # Code detection
        if any(c in query for c in ["def ", "class ", "import "]):
            complexity += 2.0
        
        return min(complexity, 10.0)


class BatchInferenceEngine:
    """
    Process multiple queries efficiently
    - Batch similar queries together
    - Use smallest sufficient model
    - Maximize GPU utilization
    """
    
    def __init__(self, batch_size: int = 512):
        self.batch_size = batch_size
        self.query_queue = []
        self.complexity_analyzer = QueryComplexityAnalyzer()
        self.batch_history = []
        self.stats = {
            "total_queries": 0,
            "total_batches": 0,
            "avg_batch_size": 0,
            "model_usage": {}
        }
    
    def add_query(self, query_id: str, query: str, priority: int = 5) -> BatchQuery:
        """Add query to batch queue"""
        complexity = self.complexity_analyzer.analyze(query)
        
        # Determine model based on complexity
        if complexity < 3:
            model = "flash"
        elif complexity < 7:
            model = "sentinel"
        else:
            model = "oracle"
        
        batch_query = BatchQuery(
            id=query_id,
            query=query,
            complexity=complexity,
            model=model,
            priority=priority
        )
        
        self.query_queue.append(batch_query)
        self.stats["total_queries"] += 1
        
        return batch_query
    
    def classify_queries(self) -> Dict[str, List[BatchQuery]]:
        """Classify queries by complexity"""
        simple = [q for q in self.query_queue if q.complexity < 3]
        medium = [q for q in self.query_queue if 3 <= q.complexity < 7]
        complex = [q for q in self.query_queue if q.complexity >= 7]
        
        return {
            "simple": simple,
            "medium": medium,
            "complex": complex
        }
    
    async def process_batch(self, queries: List[str]) -> List[Dict]:
        """
        Smart batching and processing
        """
        print(f"\n{'='*60}")
        print(f"🎯 BATCH INFERENCE ENGINE")
        print(f"{'='*60}")
        print(f"Processing {len(queries)} queries\n")
        
        # Add queries to queue
        batch_queries = []
        for i, query in enumerate(queries):
            bq = self.add_query(f"query_{i}", query)
            batch_queries.append(bq)
        
        # Classify queries
        classified = self.classify_queries()
        
        results = []
        
        # Process simple queries with fast model
        if classified["simple"]:
            print(f"📊 SIMPLE QUERIES ({len(classified['simple'])})")
            print(f"   Model: FLASH (phi-3-mini)")
            simple_results = await self._process_batch_group(
                classified["simple"],
                "flash"
            )
            results.extend(simple_results)
        
        # Process medium queries with standard model
        if classified["medium"]:
            print(f"\n📊 MEDIUM QUERIES ({len(classified['medium'])})")
            print(f"   Model: SENTINEL (qwen2.5)")
            medium_results = await self._process_batch_group(
                classified["medium"],
                "sentinel"
            )
            results.extend(medium_results)
        
        # Process complex queries with powerful model
        if classified["complex"]:
            print(f"\n📊 COMPLEX QUERIES ({len(classified['complex'])})")
            print(f"   Model: ORACLE (deepseek-r1)")
            complex_results = await self._process_batch_group(
                classified["complex"],
                "oracle"
            )
            results.extend(complex_results)
        
        # Update stats
        self.stats["total_batches"] += 1
        if len(batch_queries) > 0:
            self.stats["avg_batch_size"] = (
                (self.stats["avg_batch_size"] * (self.stats["total_batches"] - 1) +
                 len(batch_queries)) / self.stats["total_batches"]
            )
        
        return results
    
    async def _process_batch_group(self, queries: List[BatchQuery], model_name: str) -> List[Dict]:
        """Process a group of queries with the specified model"""
        import time
        from core.ollama_client import OllamaClient
        
        # Get actual model from config
        model_config = config.OPTIMAL_MODELS.get(model_name, {})
        actual_model = model_config.get("model", config.DEFAULT_MODEL)
        
        # Create OllamaClient
        ollama = OllamaClient(model=actual_model)
        
        results = []
        for query in queries:
            start_time = time.time()
            try:
                response = await asyncio.to_thread(
                    ollama.generate,
                    query.query,
                    max_tokens=256,
                    temperature=0.3
                )
                execution_time = time.time() - start_time
                
                results.append({
                    "query": query.query,
                    "response": response,
                    "execution_time": execution_time,
                    "success": True,
                    "model": actual_model,
                    "complexity": query.complexity
                })
                
                # Update model usage stats
                if model_name not in self.stats["model_usage"]:
                    self.stats["model_usage"][model_name] = 0
                self.stats["model_usage"][model_name] += 1
                
            except Exception as e:
                execution_time = time.time() - start_time
                results.append({
                    "query": query.query,
                    "response": f"Error: {str(e)}",
                    "execution_time": execution_time,
                    "success": False,
                    "model": actual_model,
                    "complexity": query.complexity
                })
        
        return results
    
    async def _process_single_query(self, ollama, query: str) -> Dict:
        """Process a single query with timing"""
        start_time = time.time()
        try:
            response = await asyncio.to_thread(
                ollama.generate, 
                query, 
                max_tokens=256, 
                temperature=0.3
            )
            execution_time = time.time() - start_time
            
            return {
                "query": query,
                "response": response,
                "execution_time": execution_time,
                "success": True,
                "model": ollama.model
            }
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "query": query,
                "response": f"Error: {str(e)}",
                "execution_time": execution_time,
                "success": False,
                "model": ollama.model
            }
    
    def get_batch_stats(self) -> Dict:
        """Get batch processing statistics"""
        return {
            "total_queries": self.stats["total_queries"],
            "total_batches": self.stats["total_batches"],
            "avg_batch_size": self.stats["avg_batch_size"],
            "model_usage": self.stats["model_usage"],
            "queue_length": len(self.query_queue)
        }
    
    def print_batch_stats(self):
        """Print batch statistics"""
        stats = self.get_batch_stats()
        
        print(f"\n{'='*60}")
        print(f"📊 BATCH INFERENCE - STATISTICS")
        print(f"{'='*60}")
        print(f"Total Queries: {stats['total_queries']}")
        print(f"Total Batches: {stats['total_batches']}")
        print(f"Avg Batch Size: {stats['avg_batch_size']:.1f}")
        print(f"\nModel Usage:")
        for model, count in stats['model_usage'].items():
            print(f"  {model}: {count} queries")
        print(f"\nQueue Length: {stats['queue_length']}")
        print(f"{'='*60}\n")


# Example usage
if __name__ == "__main__":
    async def main():
        engine = BatchInferenceEngine()
        
        # Test queries
        test_queries = [
            "What is Python?",
            "Explain machine learning",
            "How do I write a function?",
            "What is quantum computing and how does it work?",
            "Prove that P=NP",
            "Write a simple hello world program",
            "Analyze this algorithm for efficiency",
            "What's the weather?",
            "Design a microservices architecture",
            "Debug this code: def foo(): return bar"
        ]
        
        print("🚀 BATCH INFERENCE ENGINE - TEST\n")
        
        # Process batch
        results = await engine.process_batch(test_queries)
        
        # Print results
        print("📋 RESULTS:")
        for result in results:
            print(f"  [{result['model'].upper()}] {result['query'][:40]}...")
        
        # Print stats
        engine.print_batch_stats()
    
    asyncio.run(main())
