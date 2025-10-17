"""
Tests for Genetic Evolution Engine
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from jarvisos.core.evolution import Gene, GenePool, EvolutionEngine


class TestGene:
    """Test Gene class"""
    
    def test_gene_creation(self):
        """Test creating a gene"""
        gene = Gene(
            id="test_gene_1",
            name="Test Gene",
            script_path="/path/to/script.py",
            created_at="2025-10-17T00:00:00"
        )
        assert gene.id == "test_gene_1"
        assert gene.fitness_score == 0.0
        assert gene.status == "active"
    
    def test_fitness_calculation(self):
        """Test fitness score calculation"""
        gene = Gene(
            id="test_gene_1",
            name="Test Gene",
            script_path="/path/to/script.py",
            created_at="2025-10-17T00:00:00",
            execution_count=10,
            success_count=8,
            failure_count=2,
            time_saved_seconds=300.0,
            user_rating=4
        )
        
        fitness = gene.calculate_fitness()
        assert fitness > 0
        # Update fitness score first
        gene.update_fitness()
        assert gene.fitness_score == fitness
    
    def test_record_execution_success(self):
        """Test recording successful execution"""
        gene = Gene(
            id="test_gene_1",
            name="Test Gene",
            script_path="/path/to/script.py",
            created_at="2025-10-17T00:00:00"
        )
        
        gene.record_execution(success=True, time_saved=10.0)
        assert gene.execution_count == 1
        assert gene.success_count == 1
        assert gene.failure_count == 0
        assert gene.time_saved_seconds == 10.0
    
    def test_record_execution_failure(self):
        """Test recording failed execution"""
        gene = Gene(
            id="test_gene_1",
            name="Test Gene",
            script_path="/path/to/script.py",
            created_at="2025-10-17T00:00:00"
        )
        
        gene.record_execution(success=False)
        assert gene.execution_count == 1
        assert gene.success_count == 0
        assert gene.failure_count == 1


class TestGenePool:
    """Test GenePool class"""
    
    @pytest.fixture
    def temp_pool_dir(self):
        """Create temporary pool directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_gene_pool_creation(self, temp_pool_dir):
        """Test creating gene pool"""
        pool = GenePool(pool_dir=temp_pool_dir)
        assert pool.pool_dir.exists()
    
    def test_add_gene(self, temp_pool_dir):
        """Test adding gene to pool"""
        pool = GenePool(pool_dir=temp_pool_dir)
        
        gene = Gene(
            id="test_gene_1",
            name="Test Gene",
            script_path="/path/to/script.py",
            created_at="2025-10-17T00:00:00"
        )
        
        pool.add_gene(gene)
        loaded_gene = pool.get_gene("test_gene_1")
        
        assert loaded_gene is not None
        assert loaded_gene.id == "test_gene_1"
    
    def test_get_active_genes(self, temp_pool_dir):
        """Test getting active genes"""
        pool = GenePool(pool_dir=temp_pool_dir)
        
        # Add active gene
        gene1 = Gene(
            id="active_1",
            name="Active Gene",
            script_path="/path/to/script.py",
            created_at="2025-10-17T00:00:00",
            status="active"
        )
        pool.add_gene(gene1)
        
        # Add dormant gene
        gene2 = Gene(
            id="dormant_1",
            name="Dormant Gene",
            script_path="/path/to/script.py",
            created_at="2025-10-17T00:00:00",
            status="dormant"
        )
        pool.add_gene(gene2)
        
        active_genes = pool.get_active_genes()
        assert len(active_genes) == 1
        assert active_genes[0].id == "active_1"
    
    def test_natural_selection(self, temp_pool_dir):
        """Test natural selection removes weak genes"""
        pool = GenePool(pool_dir=temp_pool_dir)
        
        # Add gene with low fitness
        gene = Gene(
            id="weak_gene",
            name="Weak Gene",
            script_path="/path/to/script.py",
            created_at="2025-10-17T00:00:00",
            fitness_score=0.1,
            execution_count=100,
            success_count=10,
            failure_count=90
        )
        pool.add_gene(gene)
        
        # natural_selection takes 'threshold' not 'fitness_threshold'
        pool.natural_selection(threshold=0.3)
        
        loaded_gene = pool.get_gene("weak_gene")
        assert loaded_gene.status == "extinct"


class TestEvolutionEngine:
    """Test EvolutionEngine class"""
    
    @pytest.fixture
    def temp_pool_dir(self):
        """Create temporary pool directory"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_evolution_engine_creation(self, temp_pool_dir):
        """Test creating evolution engine"""
        pool = GenePool(pool_dir=temp_pool_dir)
        engine = EvolutionEngine(gene_pool=pool)
        assert engine.gene_pool == pool
    
    def test_selection(self, temp_pool_dir):
        """Test selecting top genes"""
        pool = GenePool(pool_dir=temp_pool_dir)
        engine = EvolutionEngine(gene_pool=pool)
        
        # Add genes with different fitness
        for i in range(5):
            gene = Gene(
                id=f"gene_{i}",
                name=f"Gene {i}",
                script_path="/path/to/script.py",
                created_at="2025-10-17T00:00:00",
                fitness_score=float(i)
            )
            pool.add_gene(gene)
        
        # selection() doesn't take parameters, it returns top 10
        selected = engine.selection()
        assert len(selected) <= 10
        assert len(selected) > 0
        # Should be sorted by fitness (descending)
        if len(selected) > 1:
            assert selected[0].fitness_score >= selected[1].fitness_score
    
    def test_evolve(self, temp_pool_dir):
        """Test evolution cycle"""
        pool = GenePool(pool_dir=temp_pool_dir)
        engine = EvolutionEngine(gene_pool=pool)
        
        # Add some genes
        for i in range(3):
            gene = Gene(
                id=f"gene_{i}",
                name=f"Gene {i}",
                script_path="/path/to/script.py",
                created_at="2025-10-17T00:00:00",
                fitness_score=float(i) + 1.0,
                execution_count=10,
                success_count=8
            )
            pool.add_gene(gene)
        
        result = engine.evolve()
        assert "mutations_created" in result
        assert "genes_selected" in result
