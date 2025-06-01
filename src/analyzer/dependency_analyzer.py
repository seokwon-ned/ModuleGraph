from pathlib import Path
from typing import Dict, List, Set
from .gradle_parser import GradleParser

class DependencyAnalyzer:
    def __init__(self, project_root: Path, modules: Set[str]):
        self.project_root = project_root
        self.modules = modules
        self.parser = GradleParser(project_root)
        
    def analyze_dependencies(self) -> Dict[str, List[str]]:
        """모든 모듈의 의존성을 분석합니다."""
        dependencies = {}
        
        for module in self.modules:
            # 각 모듈의 build.gradle 파일에서 의존성 추출
            deps = self.parser.parse_build_gradle(module)
            # 실제 존재하는 모듈에 대한 의존성만 필터링
            valid_deps = [dep for dep in deps if dep in self.modules]
            dependencies[module] = valid_deps
            
        return dependencies
    
    def find_cycles(self) -> List[List[str]]:
        """순환 의존성을 찾습니다."""
        def dfs(module: str, visited: Set[str], path: List[str], cycles: List[List[str]]):
            if module in path:
                cycle_start = path.index(module)
                cycles.append(path[cycle_start:] + [module])
                return
                
            if module in visited:
                return
                
            visited.add(module)
            path.append(module)
            
            for dep in self.analyze_dependencies().get(module, []):
                dfs(dep, visited, path, cycles)
                
            path.pop()
            
        cycles = []
        visited = set()
        
        for module in self.modules:
            if module not in visited:
                dfs(module, visited, [], cycles)
                
        return cycles 