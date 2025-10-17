#!/usr/bin/env python3
"""
JarvisOS - Self-Improvement Engine
Le système qui s'améliore automatiquement

Tourne en background et:
1. Observe les patterns de commandes
2. Détecte les répétitions
3. Génère des automatisations
4. Propose des améliorations
5. Apprend de tes feedbacks
"""

import time
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class SelfImprover:
    """
    Moteur d'auto-amélioration de JarvisOS
    
    Principe:
    - Analyse automatique des observations
    - Détection de patterns répétitifs
    - Génération d'améliorations
    - Apprentissage continu
    """
    
    def __init__(self):
        self.data_dir = Path.home() / ".jarvisos"
        self.data_dir.mkdir(exist_ok=True)
        
        self.observations_file = self.data_dir / "observations.json"
        self.improvements_file = self.data_dir / "improvements.json"
        self.patterns_file = self.data_dir / "patterns.json"
        
        self.threshold = 5  # Nombre de répétitions avant action
        self.ai = None  # Lazy load
        
    def run_forever(self):
        """
        Boucle principale d'amélioration continue
        Tourne en background comme service
        """
        print("🧬 JarvisOS Self-Improvement Engine started")
        print(f"   Monitoring: {self.observations_file}")
        print(f"   Threshold: {self.threshold} repetitions")
        print()
        
        iteration = 0
        
        while True:
            try:
                iteration += 1
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Iteration #{iteration}")
                
                # 1. Analyse les observations
                patterns = self.detect_patterns()
                
                if patterns:
                    print(f"   🔍 Found {len(patterns)} patterns")
                    
                    # 2. Génère des améliorations
                    for pattern in patterns:
                        self.improve_from_pattern(pattern)
                else:
                    print("   ✓ No new patterns detected")
                
                # 3. Attends avant prochain cycle
                print(f"   💤 Sleeping 1 hour...\n")
                time.sleep(3600)  # 1 heure
                
            except KeyboardInterrupt:
                print("\n🛑 Self-Improvement Engine stopped by user")
                break
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
                print("   Retrying in 5 minutes...")
                time.sleep(300)
    
    def detect_patterns(self) -> List[Dict]:
        """
        Détecte les patterns répétitifs dans les observations
        
        Returns:
            Liste de patterns trouvés
        """
        if not self.observations_file.exists():
            return []
        
        try:
            with open(self.observations_file) as f:
                observations = json.load(f)
        except:
            return []
        
        # Analyse des commandes
        command_counts = {}
        command_contexts = {}
        
        for obs in observations:
            cmd = obs.get('command', '').strip()
            if not cmd:
                continue
            
            # Compte les occurrences
            if cmd not in command_counts:
                command_counts[cmd] = 0
                command_contexts[cmd] = []
            
            command_counts[cmd] += 1
            command_contexts[cmd].append(obs)
        
        # Identifie les patterns (répétitions > threshold)
        patterns = []
        for cmd, count in command_counts.items():
            if count >= self.threshold:
                pattern = {
                    'command': cmd,
                    'count': count,
                    'contexts': command_contexts[cmd],
                    'detected_at': datetime.now().isoformat(),
                    'type': self._classify_pattern(cmd)
                }
                
                # Vérifie si déjà traité
                if not self._is_pattern_processed(pattern):
                    patterns.append(pattern)
        
        return patterns
    
    def _classify_pattern(self, command: str) -> str:
        """Classifie le type de pattern"""
        cmd_lower = command.lower()
        
        if 'git' in cmd_lower:
            return 'git_workflow'
        elif 'docker' in cmd_lower or 'compose' in cmd_lower:
            return 'docker_ops'
        elif 'npm' in cmd_lower or 'yarn' in cmd_lower:
            return 'node_dev'
        elif 'python' in cmd_lower or 'pip' in cmd_lower:
            return 'python_dev'
        elif 'test' in cmd_lower:
            return 'testing'
        else:
            return 'general'
    
    def _is_pattern_processed(self, pattern: Dict) -> bool:
        """Vérifie si un pattern a déjà été traité"""
        if not self.patterns_file.exists():
            return False
        
        try:
            with open(self.patterns_file) as f:
                processed = json.load(f)
            
            # Check si commande déjà vue
            for p in processed:
                if p['command'] == pattern['command']:
                    return True
            
            return False
        except:
            return False
    
    def improve_from_pattern(self, pattern: Dict):
        """
        Génère une amélioration basée sur un pattern détecté
        
        Args:
            pattern: Pattern à améliorer
        """
        print(f"\n   💡 New improvement opportunity:")
        print(f"      Command: {pattern['command']}")
        print(f"      Repeated: {pattern['count']}x")
        print(f"      Type: {pattern['type']}")
        
        # Génère suggestion d'amélioration
        improvement = {
            'id': self._generate_id(),
            'pattern': pattern,
            'suggestion': self._generate_suggestion(pattern),
            'created_at': datetime.now().isoformat(),
            'status': 'pending',
            'risk_level': self._assess_risk(pattern)
        }
        
        # Sauvegarde
        self._save_improvement(improvement)
        
        # Marque pattern comme traité
        self._mark_pattern_processed(pattern)
        
        print(f"      Status: Saved as improvement #{improvement['id']}")
        print(f"      Risk: {improvement['risk_level']}")
        print(f"      → Run 'jarvis improvements' to review\n")
    
    def _generate_suggestion(self, pattern: Dict) -> str:
        """
        Génère une suggestion d'amélioration
        
        Pour v0.1: Suggestions simples
        Pour v1.0: Utiliser AI pour générer code
        """
        cmd = pattern['command']
        count = pattern['count']
        ptype = pattern['type']
        
        suggestions = {
            'git_workflow': f"Create alias 'g{cmd.split()[1]}' for '{cmd}'",
            'docker_ops': f"Create script 'docker-{cmd.split()[1]}.sh' to automate",
            'python_dev': f"Add to Makefile: 'make {cmd.split()[1]}'",
            'testing': f"Create pre-commit hook for '{cmd}'",
            'general': f"Create bash alias for '{cmd}'"
        }
        
        base_suggestion = suggestions.get(ptype, suggestions['general'])
        
        return f"{base_suggestion}\n\nYou run this {count} times. Automation would save ~{count * 5} seconds."
    
    def _assess_risk(self, pattern: Dict) -> str:
        """Évalue le niveau de risque"""
        cmd = pattern['command'].lower()
        
        dangerous = ['rm', 'delete', 'drop', 'truncate', 'format']
        moderate = ['sudo', 'chmod', 'chown', 'mv']
        
        if any(d in cmd for d in dangerous):
            return 'high'
        elif any(m in cmd for m in moderate):
            return 'moderate'
        else:
            return 'low'
    
    def _generate_id(self) -> str:
        """Génère un ID unique"""
        return datetime.now().strftime('%Y%m%d%H%M%S')
    
    def _save_improvement(self, improvement: Dict):
        """Sauvegarde une amélioration"""
        improvements = []
        if self.improvements_file.exists():
            try:
                with open(self.improvements_file) as f:
                    improvements = json.load(f)
            except:
                improvements = []
        
        improvements.append(improvement)
        
        with open(self.improvements_file, 'w') as f:
            json.dump(improvements, f, indent=2)
    
    def _mark_pattern_processed(self, pattern: Dict):
        """Marque un pattern comme traité"""
        processed = []
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file) as f:
                    processed = json.load(f)
            except:
                processed = []
        
        processed.append({
            'command': pattern['command'],
            'processed_at': datetime.now().isoformat()
        })
        
        with open(self.patterns_file, 'w') as f:
            json.dump(processed, f, indent=2)
    
    def get_improvements(self, status: Optional[str] = None) -> List[Dict]:
        """
        Récupère les améliorations
        
        Args:
            status: Filtrer par statut (pending, approved, rejected)
        """
        if not self.improvements_file.exists():
            return []
        
        try:
            with open(self.improvements_file) as f:
                improvements = json.load(f)
            
            if status:
                improvements = [i for i in improvements if i['status'] == status]
            
            return improvements
        except:
            return []


def run_as_service():
    """Lance le self-improver comme service"""
    improver = SelfImprover()
    improver.run_forever()


if __name__ == "__main__":
    run_as_service()
