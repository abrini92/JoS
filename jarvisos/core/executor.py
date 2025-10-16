"""
Executor - Safely executes generated automation scripts
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.syntax import Syntax
from rich.table import Table

console = Console()


class Executor:
    """Safely executes generated automation scripts"""

    def __init__(self, scripts_dir: str = "generated_scripts"):
        self.scripts_dir = Path(scripts_dir)
        if not self.scripts_dir.exists():
            self.scripts_dir.mkdir(exist_ok=True)

    def list_scripts(self) -> List[Path]:
        """List all available scripts"""
        scripts = list(self.scripts_dir.glob("*.py"))
        return sorted(scripts)

    def display_scripts(self) -> None:
        """Display available scripts in a table"""
        scripts = self.list_scripts()
        
        if not scripts:
            console.print("\n[yellow]⚠️  No scripts found in generated_scripts/[/yellow]")
            console.print("Run 'jarvis generate' first to create automation scripts.\n")
            return
        
        console.print("\n[bold cyan]📜 Available Scripts:[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=4)
        table.add_column("Script Name", style="green")
        table.add_column("Size", style="yellow", width=10)
        table.add_column("Modified", style="white")
        
        for i, script in enumerate(scripts, 1):
            stat = script.stat()
            size = f"{stat.st_size} bytes"
            modified = script.stat().st_mtime
            from datetime import datetime
            modified_str = datetime.fromtimestamp(modified).strftime("%Y-%m-%d %H:%M")
            
            table.add_row(str(i), script.name, size, modified_str)
        
        console.print(table)
        console.print()

    def preview_script(self, script_path: Path) -> None:
        """Preview script content with syntax highlighting"""
        console.print(f"\n[bold yellow]📄 Preview: {script_path.name}[/bold yellow]\n")
        
        with open(script_path, 'r') as f:
            code = f.read()
        
        # Show first 50 lines for preview
        lines = code.split('\n')
        preview_lines = lines[:50]
        preview_code = '\n'.join(preview_lines)
        
        if len(lines) > 50:
            preview_code += f"\n\n... ({len(lines) - 50} more lines)"
        
        syntax = Syntax(preview_code, "python", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, border_style="cyan"))
        console.print()

    def get_script_by_id(self, script_id: int) -> Optional[Path]:
        """Get script by ID (1-indexed)"""
        scripts = self.list_scripts()
        
        if script_id < 1 or script_id > len(scripts):
            console.print(f"[bold red]❌ Invalid script ID: {script_id}[/bold red]")
            console.print(f"Available IDs: 1-{len(scripts)}\n")
            return None
        
        return scripts[script_id - 1]

    def get_script_by_name(self, name: str) -> Optional[Path]:
        """Get script by name"""
        script_path = self.scripts_dir / name
        
        if not script_path.exists():
            console.print(f"[bold red]❌ Script not found: {name}[/bold red]\n")
            return None
        
        return script_path

    def execute_script(
        self, 
        script_path: Path, 
        dry_run: bool = False,
        timeout: int = 30
    ) -> Dict:
        """
        Execute a script safely
        
        Args:
            script_path: Path to the script
            dry_run: If True, only preview without executing
            timeout: Maximum execution time in seconds
        
        Returns:
            Dict with execution results
        """
        console.print(f"\n[bold cyan]🚀 Preparing to execute: {script_path.name}[/bold cyan]\n")
        
        # Preview script
        self.preview_script(script_path)
        
        if dry_run:
            console.print("[bold yellow]🔍 DRY RUN MODE - Script not executed[/bold yellow]\n")
            return {'status': 'dry_run', 'script': str(script_path)}
        
        # Ask for confirmation
        console.print("[bold yellow]⚠️  You are about to execute this script.[/bold yellow]")
        console.print("Please review the code above carefully.\n")
        
        if not Confirm.ask("Do you want to proceed?", default=False):
            console.print("\n[yellow]❌ Execution cancelled by user[/yellow]\n")
            return {'status': 'cancelled', 'script': str(script_path)}
        
        # Execute script
        console.print(f"\n[bold green]▶️  Executing script...[/bold green]")
        console.print(f"Timeout: {timeout}s\n")
        console.print("="*70)
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=script_path.parent
            )
            
            console.print("="*70)
            
            # Display output
            if result.stdout:
                console.print("\n[bold green]📤 Output:[/bold green]")
                console.print(result.stdout)
            
            if result.stderr:
                console.print("\n[bold red]⚠️  Errors/Warnings:[/bold red]")
                console.print(result.stderr)
            
            # Check return code
            if result.returncode == 0:
                console.print("\n[bold green]✅ Script executed successfully![/bold green]\n")
                status = 'success'
            else:
                console.print(f"\n[bold red]❌ Script failed with exit code: {result.returncode}[/bold red]\n")
                status = 'failed'
            
            return {
                'status': status,
                'script': str(script_path),
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            console.print("="*70)
            console.print(f"\n[bold red]⏱️  Script timed out after {timeout}s[/bold red]\n")
            return {
                'status': 'timeout',
                'script': str(script_path),
                'timeout': timeout
            }
            
        except Exception as e:
            console.print("="*70)
            console.print(f"\n[bold red]❌ Execution error: {e}[/bold red]\n")
            return {
                'status': 'error',
                'script': str(script_path),
                'error': str(e)
            }

    def run(self, script_identifier: str, dry_run: bool = False, timeout: int = 30) -> Dict:
        """
        Run a script by ID or name
        
        Args:
            script_identifier: Script ID (number) or name
            dry_run: Preview only, don't execute
            timeout: Maximum execution time in seconds
        """
        # Try to parse as ID first
        try:
            script_id = int(script_identifier)
            script_path = self.get_script_by_id(script_id)
        except ValueError:
            # Not a number, treat as name
            script_path = self.get_script_by_name(script_identifier)
        
        if not script_path:
            return {'status': 'not_found', 'identifier': script_identifier}
        
        return self.execute_script(script_path, dry_run=dry_run, timeout=timeout)


if __name__ == "__main__":
    # Quick test
    executor = Executor()
    executor.display_scripts()
