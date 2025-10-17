"""
JarvisOS Genetic Evolution Engine
Implements natural selection and evolution of automation scripts
"""

import json
import random
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

from ..utils.logger import get_logger

logger = get_logger("jarvisos.evolution")


@dataclass
class Gene:
    """Represents a script (gene) in the gene pool"""
    id: str
    name: str
    script_path: str
    created_at: str
    fitness_score: float = 0.0
    execution_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    last_executed: Optional[str] = None
    time_saved_seconds: float = 0.0
    user_rating: Optional[int] = None  # 1-5 stars
    status: str = "active"  # active, dormant, extinct
    generation: int = 1
    parent_genes: List[str] = None
    mutations: List[str] = None
    
    def __post_init__(self):
        if self.parent_genes is None:
            self.parent_genes = []
        if self.mutations is None:
            self.mutations = []
    
    def calculate_fitness(self) -> float:
        """Calculate fitness score based on multiple factors"""
        if self.execution_count == 0:
            return 0.0
        
        # Success rate (0-1)
        success_rate = self.success_count / self.execution_count if self.execution_count > 0 else 0
        
        # Usage frequency (normalized)
        usage_score = min(self.execution_count / 100, 1.0)
        
        # Time saved (normalized)
        time_score = min(self.time_saved_seconds / 3600, 1.0)  # Max 1 hour
        
        # User rating (0-1)
        rating_score = (self.user_rating / 5.0) if self.user_rating else 0.5
        
        # Weighted average
        fitness = (
            success_rate * 0.4 +
            usage_score * 0.2 +
            time_score * 0.2 +
            rating_score * 0.2
        )
        
        return round(fitness, 3)
    
    def update_fitness(self):
        """Update fitness score"""
        self.fitness_score = self.calculate_fitness()
        logger.debug(f"Gene {self.name} fitness updated: {self.fitness_score}")
    
    def record_execution(self, success: bool, time_saved: float = 0.0):
        """Record execution result"""
        self.execution_count += 1
        if success:
            self.success_count += 1
            self.time_saved_seconds += time_saved
        else:
            self.failure_count += 1
        self.last_executed = datetime.now().isoformat()
        self.update_fitness()
    
    def set_user_rating(self, rating: int):
        """Set user rating (1-5) and update fitness"""
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        self.user_rating = rating
        self.update_fitness()
        logger.info(f"Gene {self.name} rated {rating}/5, new fitness: {self.fitness_score}")


class GenePool:
    """Manages the gene pool of automation scripts"""
    
    def __init__(self, pool_dir: str = "gene_pool"):
        self.pool_dir = Path(pool_dir)
        self.pool_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.pool_dir / "active").mkdir(exist_ok=True)
        (self.pool_dir / "dormant").mkdir(exist_ok=True)
        (self.pool_dir / "extinct").mkdir(exist_ok=True)
        
        self.genes: Dict[str, Gene] = {}
        self.load_genes()
        
        logger.info(f"GenePool initialized with {len(self.genes)} genes")
    
    def load_genes(self):
        """Load all genes from gene pool"""
        for status_dir in ["active", "dormant", "extinct"]:
            status_path = self.pool_dir / status_dir
            for gene_file in status_path.glob("*.json"):
                try:
                    with open(gene_file) as f:
                        data = json.load(f)
                        gene = Gene(**data)
                        self.genes[gene.id] = gene
                except Exception as e:
                    logger.error(f"Failed to load gene {gene_file}: {e}")
    
    def save_gene(self, gene: Gene):
        """Save gene to appropriate directory"""
        status_dir = self.pool_dir / gene.status
        gene_file = status_dir / f"{gene.id}.json"
        
        with open(gene_file, 'w') as f:
            json.dump(asdict(gene), f, indent=2)
        
        logger.debug(f"Gene {gene.name} saved to {gene.status}/")
    
    def add_gene(self, gene: Gene):
        """Add new gene to pool"""
        self.genes[gene.id] = gene
        self.save_gene(gene)
        logger.info(f"New gene added: {gene.name} (fitness: {gene.fitness_score})")
    
    def get_gene(self, gene_id: str) -> Optional[Gene]:
        """Get gene by ID"""
        return self.genes.get(gene_id)
    
    def get_active_genes(self) -> List[Gene]:
        """Get all active genes"""
        return [g for g in self.genes.values() if g.status == "active"]
    
    def get_top_genes(self, n: int = 10) -> List[Gene]:
        """Get top N genes by fitness"""
        active = self.get_active_genes()
        return sorted(active, key=lambda g: g.fitness_score, reverse=True)[:n]
    
    def get_bottom_genes(self, n: int = 10) -> List[Gene]:
        """Get bottom N genes by fitness"""
        active = self.get_active_genes()
        return sorted(active, key=lambda g: g.fitness_score)[:n]
    
    def evolve_gene(self, gene: Gene, mutation_type: str) -> Gene:
        """Create mutated version of gene"""
        new_gene = Gene(
            id=f"{gene.id}_m{len(gene.mutations) + 1}",
            name=f"{gene.name} (mutated)",
            script_path=gene.script_path,
            created_at=datetime.now().isoformat(),
            generation=gene.generation + 1,
            parent_genes=[gene.id],
            mutations=[mutation_type]
        )
        
        logger.info(f"Gene evolved: {gene.name} → {new_gene.name} ({mutation_type})")
        return new_gene
    
    def natural_selection(self, threshold: float = 0.5):
        """Apply natural selection - mark low fitness genes as extinct"""
        for gene in self.get_active_genes():
            if gene.execution_count > 10 and gene.fitness_score < threshold:
                gene.status = "extinct"
                self.save_gene(gene)
                logger.info(f"Gene extinct: {gene.name} (fitness: {gene.fitness_score})")
    
    def promote_dormant(self):
        """Promote dormant genes if they might be useful"""
        dormant = [g for g in self.genes.values() if g.status == "dormant"]
        for gene in dormant:
            if gene.fitness_score > 0.7:
                gene.status = "active"
                self.save_gene(gene)
                logger.info(f"Gene promoted: {gene.name}")


class EvolutionEngine:
    """Main evolution engine - orchestrates genetic evolution"""
    
    def __init__(self, gene_pool: GenePool):
        self.gene_pool = gene_pool
        self.evolution_history: List[Dict] = []
        logger.info("EvolutionEngine initialized")
    
    def evaluate_population(self) -> Dict:
        """Evaluate current gene population"""
        active_genes = self.gene_pool.get_active_genes()
        
        if not active_genes:
            return {
                'total_genes': 0,
                'avg_fitness': 0.0,
                'top_genes': [],
                'bottom_genes': []
            }
        
        total_fitness = sum(g.fitness_score for g in active_genes)
        avg_fitness = total_fitness / len(active_genes)
        
        evaluation = {
            'timestamp': datetime.now().isoformat(),
            'total_genes': len(active_genes),
            'avg_fitness': round(avg_fitness, 3),
            'top_genes': [
                {'name': g.name, 'fitness': g.fitness_score}
                for g in self.gene_pool.get_top_genes(5)
            ],
            'bottom_genes': [
                {'name': g.name, 'fitness': g.fitness_score}
                for g in self.gene_pool.get_bottom_genes(5)
            ]
        }
        
        logger.info(f"Population evaluated: {len(active_genes)} genes, avg fitness: {avg_fitness:.3f}")
        return evaluation
    
    def selection(self) -> List[Gene]:
        """Select genes for reproduction (top performers)"""
        top_genes = self.gene_pool.get_top_genes(10)
        logger.info(f"Selected {len(top_genes)} genes for reproduction")
        return top_genes
    
    def mutation(self, gene: Gene) -> Optional[Gene]:
        """Mutate a gene (create variation)"""
        mutation_types = [
            "parameter_tweak",
            "timing_adjustment",
            "condition_modification",
            "optimization"
        ]
        
        mutation_type = random.choice(mutation_types)
        mutated_gene = self.gene_pool.evolve_gene(gene, mutation_type)
        
        return mutated_gene
    
    def crossover(self, gene1: Gene, gene2: Gene) -> Gene:
        """Combine two genes (not implemented yet - placeholder)"""
        # TODO: Implement gene crossover
        logger.debug(f"Crossover: {gene1.name} + {gene2.name}")
        return gene1
    
    def evolve(self) -> Dict:
        """Run one evolution cycle"""
        logger.info("🧬 Starting evolution cycle...")
        
        # 1. Evaluate current population
        evaluation = self.evaluate_population()
        
        # 2. Natural selection (remove weak genes)
        self.gene_pool.natural_selection(threshold=0.3)
        
        # 3. Selection (choose best genes)
        selected = self.selection()
        
        # 4. Mutation (create variations)
        mutations_created = 0
        for gene in selected[:3]:  # Mutate top 3
            if gene.fitness_score > 0.7:
                mutated = self.mutation(gene)
                if mutated:
                    self.gene_pool.add_gene(mutated)
                    mutations_created += 1
        
        # 5. Promote dormant genes
        self.gene_pool.promote_dormant()
        
        # 6. Record evolution
        evolution_record = {
            'timestamp': datetime.now().isoformat(),
            'evaluation': evaluation,
            'mutations_created': mutations_created,
            'genes_selected': len(selected)
        }
        
        self.evolution_history.append(evolution_record)
        
        logger.info(f"✅ Evolution cycle complete: {mutations_created} mutations created")
        return evolution_record
    
    def get_evolution_summary(self) -> Dict:
        """Get summary of evolution history"""
        if not self.evolution_history:
            return {'cycles': 0, 'history': []}
        
        return {
            'cycles': len(self.evolution_history),
            'latest': self.evolution_history[-1],
            'history': self.evolution_history[-10:]  # Last 10 cycles
        }


# Example usage
if __name__ == "__main__":
    # Initialize
    pool = GenePool()
    engine = EvolutionEngine(pool)
    
    # Add example gene
    example_gene = Gene(
        id="gene_001",
        name="morning_setup",
        script_path="generated_scripts/morning_setup.py",
        created_at=datetime.now().isoformat()
    )
    
    # Simulate usage
    example_gene.record_execution(success=True, time_saved=300)
    example_gene.record_execution(success=True, time_saved=300)
    example_gene.user_rating = 5
    
    pool.add_gene(example_gene)
    
    # Run evolution
    result = engine.evolve()
    print(json.dumps(result, indent=2))
