"""
Generator - Generates automation scripts based on AI insights
"""

import ast
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from anthropic import Anthropic
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

# Load environment variables from .env file
load_dotenv()

console = Console()


class Generator:
    """Generates automation scripts using Claude AI"""

    def __init__(self, data_dir: str = "data", scripts_dir: str = "generated_scripts"):
        self.data_dir = Path(data_dir)
        self.scripts_dir = Path(scripts_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.scripts_dir.mkdir(exist_ok=True)
        
        self.insights_file = self.data_dir / "insights.json"
        self.generated_tasks_file = self.data_dir / "generated_tasks.json"
        
        # Initialize Claude API
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY not found in environment variables.\n"
                "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
            )
        
        self.client = Anthropic(api_key=api_key)

    def load_insights(self) -> Dict:
        """Load insights from JSON file"""
        if not self.insights_file.exists():
            raise FileNotFoundError(
                f"❌ Insights file not found: {self.insights_file}\n"
                "Run 'jarvis analyze' first to generate insights."
            )
        
        with open(self.insights_file, 'r') as f:
            return json.load(f)

    def suggest_tasks(self, insights: Dict) -> List[Dict]:
        """Ask Claude to suggest automation tasks"""
        console.print("\n[bold cyan]🎯 Generating automation task suggestions...[/bold cyan]\n")
        
        automation_opps = insights.get('automation_opportunities', [])
        
        prompt = f"""Based on these automation opportunities identified for a user:

{json.dumps(automation_opps, indent=2)}

Suggest 3 specific automation tasks that JarvisOS should build for this user.

For each task, provide:
1. A clear task name
2. Detailed description of what it does
3. Why it's valuable for the user
4. Estimated complexity (simple/medium/complex)

Respond in JSON format:
{{
  "tasks": [
    {{
      "id": "task_1",
      "name": "Task Name",
      "description": "What it does...",
      "value": "Why it's valuable...",
      "complexity": "simple/medium/complex"
    }},
    ...
  ]
}}
"""

        try:
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            result = json.loads(response_text)
            
            return result.get('tasks', [])
            
        except Exception as e:
            console.print(f"[bold red]❌ Error generating tasks: {e}[/bold red]")
            raise

    def generate_script(self, task: Dict) -> str:
        """Generate Python script for a specific task"""
        console.print(f"\n[bold cyan]⚙️  Generating script for: {task['name']}[/bold cyan]\n")
        
        prompt = f"""You are a Python code generator for JarvisOS, a self-building operating system.

Generate a complete, production-ready Python script for this automation task:

**Task:** {task['name']}
**Description:** {task['description']}
**Value:** {task['value']}
**Complexity:** {task['complexity']}

Requirements:
1. Complete, runnable Python script
2. Include all necessary imports
3. Add error handling
4. Add logging with rich console output
5. Add docstrings
6. Make it safe to run (no destructive operations without confirmation)
7. Follow best practices

The script should be a standalone .py file that can be executed directly.

Respond with ONLY the Python code, no explanations or markdown formatting.
"""

        try:
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            
            script_code = message.content[0].text
            
            # Clean up any markdown code blocks if present
            if script_code.startswith("```python"):
                script_code = script_code.split("```python")[1]
                script_code = script_code.split("```")[0]
            elif script_code.startswith("```"):
                script_code = script_code.split("```")[1]
                script_code = script_code.split("```")[0]
            
            script_code = script_code.strip()
            
            return script_code
            
        except Exception as e:
            console.print(f"[bold red]❌ Error generating script: {e}[/bold red]")
            raise

    def validate_syntax(self, code: str) -> bool:
        """Validate Python syntax using AST"""
        try:
            ast.parse(code)
            console.print("[bold green]✅ Syntax validation passed[/bold green]")
            return True
        except SyntaxError as e:
            console.print(f"[bold red]❌ Syntax error: {e}[/bold red]")
            return False

    def save_script(self, task: Dict, code: str) -> Path:
        """Save generated script to file"""
        # Create safe filename
        filename = f"{task['id']}_{task['name'].lower().replace(' ', '_')}.py"
        script_path = self.scripts_dir / filename
        
        # Add header comment
        header = f'''"""
JarvisOS Generated Script
Task: {task['name']}
Description: {task['description']}
Generated: {datetime.now().isoformat()}
Complexity: {task['complexity']}
"""

'''
        
        full_code = header + code
        
        with open(script_path, 'w') as f:
            f.write(full_code)
        
        console.print(f"[bold green]💾 Script saved to: {script_path}[/bold green]")
        
        return script_path

    def preview_script(self, code: str, task_name: str) -> None:
        """Display script preview with syntax highlighting"""
        console.print(f"\n[bold yellow]📄 Preview: {task_name}[/bold yellow]\n")
        
        syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="Generated Script", border_style="yellow"))

    def save_task_metadata(self, tasks: List[Dict], generated_scripts: List[Dict]) -> None:
        """Save task and script metadata"""
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'total_tasks': len(tasks),
            'generated_scripts': generated_scripts
        }
        
        with open(self.generated_tasks_file, 'w') as f:
            json.dump(metadata, f, indent=2)

    def generate(self, task_index: int = 0) -> Dict:
        """
        Main generation workflow
        
        Args:
            task_index: Index of task to generate (0 = first task)
        """
        console.print("\n[bold cyan]🚀 Starting Script Generation...[/bold cyan]")
        
        # Load insights
        console.print("📂 Loading insights...")
        insights = self.load_insights()
        
        # Suggest tasks
        tasks = self.suggest_tasks(insights)
        
        if not tasks:
            console.print("[bold red]❌ No tasks suggested[/bold red]")
            return {}
        
        # Display suggested tasks
        console.print("\n[bold yellow]📋 Suggested Tasks:[/bold yellow]")
        for i, task in enumerate(tasks):
            console.print(f"\n{i+1}. [bold cyan]{task['name']}[/bold cyan]")
            console.print(f"   Description: {task['description']}")
            console.print(f"   Complexity: {task['complexity']}")
        
        # Generate script for specified task
        if task_index >= len(tasks):
            console.print(f"[bold red]❌ Invalid task index: {task_index}[/bold red]")
            return {}
        
        task = tasks[task_index]
        console.print(f"\n[bold green]✨ Generating script for task #{task_index + 1}[/bold green]")
        
        # Generate code
        code = self.generate_script(task)
        
        # Validate syntax
        if not self.validate_syntax(code):
            console.print("[bold red]❌ Generated code has syntax errors[/bold red]")
            return {}
        
        # Preview
        self.preview_script(code, task['name'])
        
        # Save script
        script_path = self.save_script(task, code)
        
        # Save metadata
        generated_scripts = [{
            'task': task,
            'script_path': str(script_path),
            'generated_at': datetime.now().isoformat()
        }]
        self.save_task_metadata(tasks, generated_scripts)
        
        console.print("\n[bold green]✅ Script generation complete![/bold green]\n")
        
        return {
            'task': task,
            'script_path': str(script_path),
            'all_tasks': tasks
        }


if __name__ == "__main__":
    # Quick test
    generator = Generator()
    generator.generate(task_index=0)
