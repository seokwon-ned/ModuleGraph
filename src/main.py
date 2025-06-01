#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import Optional

import click
from analyzer.gradle_parser import GradleParser
from analyzer.dependency_analyzer import DependencyAnalyzer
from visualizer.mermaid_generator import MermaidGenerator
from visualizer.html_generator import HtmlGenerator

@click.command()
@click.option(
    "--project-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    required=True,
    help="Android 프로젝트의 루트 디렉토리 경로",
)
@click.option(
    "--output",
    type=click.Path(file_okay=True, dir_okay=False),
    default="module_graph.html",
    help="생성될 HTML 파일의 경로",
)
def main(project_path: str, output: str) -> None:
    """Android 프로젝트의 모듈 의존성을 분석하고 시각화합니다."""
    try:
        # 프로젝트 경로 검증
        project_root = Path(project_path)
        if not (project_root / "settings.gradle").exists() and not (project_root / "settings.gradle.kts").exists():
            click.echo("Error: 유효한 Android 프로젝트가 아닙니다.", err=True)
            sys.exit(1)

        # Gradle 파일 파싱
        parser = GradleParser(project_root)
        modules = parser.parse_settings_gradle()
        
        # 의존성 분석
        analyzer = DependencyAnalyzer(project_root, modules)
        dependencies = analyzer.analyze_dependencies()
        
        # Mermaid 그래프 생성
        mermaid_gen = MermaidGenerator(dependencies)
        mermaid_graph = mermaid_gen.generate()
        
        # HTML 리포트 생성
        html_gen = HtmlGenerator(mermaid_graph)
        html_gen.generate(output)
        
        click.echo(f"분석이 완료되었습니다. 결과는 {output}에서 확인할 수 있습니다.")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 