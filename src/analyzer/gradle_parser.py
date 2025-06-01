from pathlib import Path
from typing import List, Set
import re

class GradleParser:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.settings_gradle = self._find_settings_gradle()
        
    def _find_settings_gradle(self) -> Path:
        """settings.gradle 또는 settings.gradle.kts 파일을 찾습니다."""
        for filename in ["settings.gradle", "settings.gradle.kts"]:
            path = self.project_root / filename
            if path.exists():
                return path
        raise FileNotFoundError("settings.gradle 또는 settings.gradle.kts 파일을 찾을 수 없습니다.")
    
    def parse_settings_gradle(self) -> Set[str]:
        """settings.gradle 파일에서 모듈 목록을 추출합니다."""
        modules = set()
        
        with open(self.settings_gradle, "r", encoding="utf-8") as f:
            content = f.read()
            
        # include 문에서 모듈 이름 추출
        # 예: include ':app', ':core', ':feature:login'
        include_pattern = r"include\s+['\"]([^'\"]+)['\"]"
        matches = re.finditer(include_pattern, content)
        
        for match in matches:
            module_path = match.group(1)
            # 모듈 경로에서 실제 모듈 이름 추출
            # 예: ':feature:login' -> 'feature:login'
            module_name = module_path.lstrip(":")
            modules.add(module_name)
            
        return modules
    
    def parse_build_gradle(self, module_name: str) -> List[str]:
        """build.gradle 파일에서 의존성을 추출합니다."""
        module_path = self.project_root / module_name.replace(":", "/")
        build_gradle = module_path / "build.gradle"
        build_gradle_kts = module_path / "build.gradle.kts"
        
        # build.gradle 또는 build.gradle.kts 파일 찾기
        gradle_file = build_gradle if build_gradle.exists() else build_gradle_kts
        if not gradle_file.exists():
            return []
            
        dependencies = []
        with open(gradle_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # implementation, api, compileOnly 등의 의존성 추출
        # 예: implementation project(':core')
        dep_pattern = r"(?:implementation|api|compileOnly)\s+project\(['\"]([^'\"]+)['\"]\)"
        matches = re.finditer(dep_pattern, content)
        
        for match in matches:
            dep_path = match.group(1)
            # 의존성 경로에서 실제 모듈 이름 추출
            # 예: ':core' -> 'core'
            dep_name = dep_path.lstrip(":")
            dependencies.append(dep_name)
            
        return dependencies 