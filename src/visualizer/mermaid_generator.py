from typing import Dict, List

class MermaidGenerator:
    def __init__(self, dependencies: Dict[str, List[str]]):
        self.dependencies = dependencies
        
    def generate(self) -> str:
        """의존성 정보를 Mermaid 그래프 문법으로 변환합니다."""
        lines = ["graph TD"]
        
        # 노드 정의
        for module in self.dependencies.keys():
            # 모듈 이름에 특수문자가 있는 경우 처리
            safe_name = self._sanitize_node_name(module)
            lines.append(f"    {safe_name}[\"{module}\"]")
            
        # 엣지 정의
        for module, deps in self.dependencies.items():
            from_node = self._sanitize_node_name(module)
            for dep in deps:
                to_node = self._sanitize_node_name(dep)
                lines.append(f"    {from_node} --> {to_node}")
                
        return "\n".join(lines)
    
    def _sanitize_node_name(self, name: str) -> str:
        """Mermaid 노드 이름으로 사용할 수 있도록 문자열을 변환합니다."""
        # 특수문자를 언더스코어로 변환
        sanitized = "".join(c if c.isalnum() else "_" for c in name)
        # 숫자로 시작하는 경우 'm_' 접두어 추가
        if sanitized[0].isdigit():
            sanitized = "m_" + sanitized
        return sanitized 