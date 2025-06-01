from pathlib import Path
from jinja2 import Environment, FileSystemLoader

class HtmlGenerator:
    def __init__(self, mermaid_graph: str):
        self.mermaid_graph = mermaid_graph
        self.template_dir = Path(__file__).parent.parent.parent / "templates"
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))
        
    def generate(self, output_path: str) -> None:
        """Mermaid 그래프를 포함한 HTML 리포트를 생성합니다."""
        template = self.env.get_template("report.html")
        html_content = template.render(
            mermaid_graph=self.mermaid_graph,
            title="Android Module Dependency Graph"
        )
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content) 