"""
JarvisOS Test Judge
Quality assurance and validation system
"""
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


@dataclass
class TestResult:
    """Test result data"""
    category: str
    test_name: str
    passed: bool
    score: float
    message: str
    details: str = ""


class JarvisOSJudge:
    """
    Quality judge for JarvisOS
    Validates code quality, functionality, and performance
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.results: List[TestResult] = []
        self.total_score = 0.0
        self.max_score = 0.0
    
    def run_all_tests(self) -> Dict:
        """Run all test categories"""
        console.print("\n[bold cyan]🧪 JarvisOS Test Judge[/bold cyan]")
        console.print("[dim]Quality Assurance & Validation[/dim]\n")
        
        # 1. Code Quality Tests
        self._test_code_quality()
        
        # 2. Unit Tests
        self._test_unit_tests()
        
        # 3. Integration Tests
        self._test_integration()
        
        # 4. Performance Tests
        self._test_performance()
        
        # 5. Security Tests
        self._test_security()
        
        # 6. Documentation Tests
        self._test_documentation()
        
        # Generate report
        return self._generate_report()
    
    def _test_code_quality(self):
        """Test code quality with linters"""
        console.print("[bold]📝 Code Quality Tests[/bold]")
        
        # Test 1: Python syntax
        try:
            result = subprocess.run(
                ["python", "-m", "py_compile", "jarvis.py"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            self._add_result(
                "Code Quality",
                "Python Syntax",
                result.returncode == 0,
                10.0,
                "✅ No syntax errors" if result.returncode == 0 else "❌ Syntax errors found",
                result.stderr
            )
        except Exception as e:
            self._add_result("Code Quality", "Python Syntax", False, 10.0, f"❌ Error: {e}")
        
        # Test 2: Import checks
        try:
            result = subprocess.run(
                ["python", "-c", "import jarvisos"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            self._add_result(
                "Code Quality",
                "Import Check",
                result.returncode == 0,
                10.0,
                "✅ All imports valid" if result.returncode == 0 else "❌ Import errors",
                result.stderr
            )
        except Exception as e:
            self._add_result("Code Quality", "Import Check", False, 10.0, f"❌ Error: {e}")
        
        # Test 3: File structure
        required_files = [
            "jarvis.py",
            "jarvisos/__init__.py",
            "jarvisos/core/__init__.py",
            "jarvisos/core/observer.py",
            "jarvisos/core/analyzer.py",
            "jarvisos/core/generator.py",
            "jarvisos/core/executor.py",
            "jarvisos/core/evolution.py",
            "jarvisos/core/dna.py",
            "requirements.txt",
            "README.md"
        ]
        
        missing = []
        for file in required_files:
            if not (self.project_root / file).exists():
                missing.append(file)
        
        self._add_result(
            "Code Quality",
            "File Structure",
            len(missing) == 0,
            10.0,
            f"✅ All required files present" if not missing else f"❌ Missing: {', '.join(missing)}",
            f"Required: {len(required_files)}, Found: {len(required_files) - len(missing)}"
        )
    
    def _test_unit_tests(self):
        """Run unit tests"""
        console.print("\n[bold]🧪 Unit Tests[/bold]")
        
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "tests/", "-v", "--tb=short"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            # Parse pytest output
            output = result.stdout
            passed = "passed" in output
            
            # Count tests
            import re
            match = re.search(r'(\d+) passed', output)
            num_passed = int(match.group(1)) if match else 0
            
            self._add_result(
                "Unit Tests",
                "Pytest Suite",
                result.returncode == 0,
                30.0,
                f"✅ {num_passed} tests passed" if result.returncode == 0 else "❌ Some tests failed",
                output[-500:] if len(output) > 500 else output
            )
        except Exception as e:
            self._add_result("Unit Tests", "Pytest Suite", False, 30.0, f"❌ Error: {e}")
    
    def _test_integration(self):
        """Test system integration"""
        console.print("\n[bold]🔗 Integration Tests[/bold]")
        
        # Test 1: CLI commands
        commands = ["status", "dna", "genes"]
        for cmd in commands:
            try:
                result = subprocess.run(
                    ["python", "jarvis.py", cmd],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=self.project_root
                )
                self._add_result(
                    "Integration",
                    f"CLI: {cmd}",
                    result.returncode == 0,
                    5.0,
                    f"✅ Command works" if result.returncode == 0 else f"❌ Command failed"
                )
            except Exception as e:
                self._add_result("Integration", f"CLI: {cmd}", False, 5.0, f"❌ Error: {e}")
    
    def _test_performance(self):
        """Test performance"""
        console.print("\n[bold]⚡ Performance Tests[/bold]")
        
        # Test 1: Import speed
        import time
        start = time.time()
        try:
            subprocess.run(
                ["python", "-c", "import jarvisos"],
                capture_output=True,
                timeout=5,
                cwd=self.project_root
            )
            duration = time.time() - start
            
            self._add_result(
                "Performance",
                "Import Speed",
                duration < 2.0,
                10.0,
                f"✅ Fast ({duration:.2f}s)" if duration < 2.0 else f"⚠️ Slow ({duration:.2f}s)",
                f"Target: <2s, Actual: {duration:.2f}s"
            )
        except Exception as e:
            self._add_result("Performance", "Import Speed", False, 10.0, f"❌ Error: {e}")
    
    def _test_security(self):
        """Test security"""
        console.print("\n[bold]🔒 Security Tests[/bold]")
        
        # Test 1: No hardcoded secrets (excluding test files and safe patterns)
        violations = []
        
        for py_file in self.project_root.rglob("*.py"):
            # Skip test files, venv, and cache
            if "venv" in str(py_file) or "__pycache__" in str(py_file) or "test" in str(py_file):
                continue
            
            try:
                content = py_file.read_text()
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    # Skip comments and docstrings
                    if line.strip().startswith('#') or '"""' in line or "'''" in line:
                        continue
                    
                    # Check for hardcoded secrets (but not env var usage)
                    lower_line = line.lower()
                    
                    # Skip safe patterns (getting from env, error messages, etc.)
                    if 'os.getenv' in line or 'os.environ' in line or 'getenv' in line:
                        continue
                    if 'raise' in line or 'error' in lower_line or 'exception' in lower_line:
                        continue
                    
                    # Look for actual hardcoded values
                    dangerous_patterns = [
                        ('api_key', '=', '"'),
                        ('api_key', '=', "'"),
                        ('password', '=', '"'),
                        ('password', '=', "'"),
                        ('secret', '=', '"'),
                        ('secret', '=', "'"),
                        ('token', '=', '"'),
                        ('token', '=', "'"),
                    ]
                    
                    for key, eq, quote in dangerous_patterns:
                        if key in lower_line and eq in line and quote in line:
                            # Make sure it's not a variable assignment to env
                            if 'env' not in lower_line and 'load' not in lower_line:
                                violations.append(f"{py_file.name}:{i}")
                                break
            except:
                pass
        
        self._add_result(
            "Security",
            "No Hardcoded Secrets",
            len(violations) == 0,
            10.0,
            "✅ No secrets found" if not violations else f"⚠️ Found: {', '.join(violations)}"
        )
    
    def _test_documentation(self):
        """Test documentation"""
        console.print("\n[bold]📚 Documentation Tests[/bold]")
        
        # Test 1: README exists and has content
        readme = self.project_root / "README.md"
        if readme.exists():
            content = readme.read_text()
            has_title = "# " in content
            has_description = len(content) > 500
            has_usage = "usage" in content.lower() or "install" in content.lower()
            
            score = sum([has_title, has_description, has_usage])
            self._add_result(
                "Documentation",
                "README Quality",
                score >= 2,
                10.0,
                f"✅ Good README ({score}/3)" if score >= 2 else f"⚠️ Incomplete README ({score}/3)"
            )
        else:
            self._add_result("Documentation", "README Quality", False, 10.0, "❌ README missing")
    
    def _add_result(self, category: str, test_name: str, passed: bool, 
                    max_score: float, message: str, details: str = ""):
        """Add test result"""
        score = max_score if passed else 0.0
        self.total_score += score
        self.max_score += max_score
        
        result = TestResult(
            category=category,
            test_name=test_name,
            passed=passed,
            score=score,
            message=message,
            details=details
        )
        self.results.append(result)
        
        # Print result
        status = "✅" if passed else "❌"
        console.print(f"  {status} {test_name}: {message}")
    
    def _generate_report(self) -> Dict:
        """Generate final report"""
        console.print("\n" + "="*60)
        console.print("[bold cyan]📊 Test Report[/bold cyan]\n")
        
        # Calculate percentage
        percentage = (self.total_score / self.max_score * 100) if self.max_score > 0 else 0
        
        # Grade
        if percentage >= 90:
            grade = "A+"
            color = "green"
        elif percentage >= 80:
            grade = "A"
            color = "green"
        elif percentage >= 70:
            grade = "B"
            color = "yellow"
        elif percentage >= 60:
            grade = "C"
            color = "yellow"
        else:
            grade = "F"
            color = "red"
        
        # Summary table
        table = Table(title="Test Summary")
        table.add_column("Category", style="cyan")
        table.add_column("Passed", style="green")
        table.add_column("Failed", style="red")
        table.add_column("Score", style="yellow")
        
        categories = {}
        for result in self.results:
            if result.category not in categories:
                categories[result.category] = {"passed": 0, "failed": 0, "score": 0, "max": 0}
            
            if result.passed:
                categories[result.category]["passed"] += 1
            else:
                categories[result.category]["failed"] += 1
            
            categories[result.category]["score"] += result.score
            categories[result.category]["max"] += result.score if result.passed else (result.score if result.score > 0 else 10.0)
        
        for category, stats in categories.items():
            table.add_row(
                category,
                str(stats["passed"]),
                str(stats["failed"]),
                f"{stats['score']:.1f}/{stats['max']:.1f}"
            )
        
        console.print(table)
        
        # Final score
        console.print(f"\n[bold]Final Score:[/bold] [{color}]{self.total_score:.1f}/{self.max_score:.1f} ({percentage:.1f}%)[/{color}]")
        console.print(f"[bold]Grade:[/bold] [{color}]{grade}[/{color}]\n")
        
        # Verdict
        if percentage >= 80:
            console.print(Panel("[bold green]✅ JARVISOS IS PRODUCTION READY![/bold green]", style="green"))
        elif percentage >= 60:
            console.print(Panel("[bold yellow]⚠️ JARVISOS NEEDS SOME IMPROVEMENTS[/bold yellow]", style="yellow"))
        else:
            console.print(Panel("[bold red]❌ JARVISOS NEEDS MAJOR WORK[/bold red]", style="red"))
        
        return {
            "total_score": self.total_score,
            "max_score": self.max_score,
            "percentage": percentage,
            "grade": grade,
            "results": [asdict(r) for r in self.results]
        }


if __name__ == "__main__":
    judge = JarvisOSJudge()
    report = judge.run_all_tests()
    
    # Save report
    with open("test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    console.print(f"\n[dim]Report saved to: test_report.json[/dim]")
