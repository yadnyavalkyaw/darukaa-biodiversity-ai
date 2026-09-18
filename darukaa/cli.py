"""Command-Line Interface (CLI) for Darukaa.Earth AI Biodiversity Intelligence.

Allows evaluators and researchers to run interactive multi-turn conversations,
execute structured benchmark analyses, and inspect the retrievable knowledge layer directly in terminal.
"""

from __future__ import annotations

import argparse
import json
import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

from darukaa.dialogue import ClarificationEngine, ParameterExtractor, SessionStore
from darukaa.engine import (
    ClimateMetrics,
    EnvironmentalReasoner,
    EnvironmentalState,
    LandUseMetrics,
    SoilMetrics,
)
from darukaa.knowledge import KnowledgeRetriever

console = Console()


def run_benchmark_mode() -> None:
    """Executes the exact hackathon reference scenario and prints scientific reasoning."""
    console.print(
        Panel.fit(
            "[bold green]Darukaa.Earth AI Biodiversity Intelligence[/bold green]\n"
            "[cyan]Running Hackathon Benchmark Case: Semi-Arid Monoculture Wheat[/cyan]",
            border_style="green",
        )
    )

    state = EnvironmentalState(
        region_name="semi-arid",
        soil=SoilMetrics(organic_carbon_pct=0.3),
        climate=ClimateMetrics(rainfall_category="low", annual_rainfall_mm=320.0),
        land_use=LandUseMetrics(crop_system="monoculture wheat", land_type="cropland"),
    )

    reasoner = EnvironmentalReasoner()
    result = reasoner.analyze(state)

    console.print(f"\n[bold]Parcel Summary:[/bold] {result.parcel_summary}")
    console.print(
        f"[bold]Active Environmental Variables:[/bold] {', '.join(result.variable_connections)}"
    )

    # Vulnerabilities Table
    vuln_table = Table(title="Critical Ecological Vulnerabilities", border_style="red")
    vuln_table.add_column("No.", style="dim", width=4)
    vuln_table.add_column("Vulnerability Analysis", style="yellow")
    for i, v in enumerate(result.critical_vulnerabilities, 1):
        vuln_table.add_row(str(i), v)
    console.print(vuln_table)

    # Recommendations
    for rec in result.recommendations:
        rec_content = [
            f"[bold cyan]Action:[/bold cyan] {rec.primary_action}\n",
            f"[bold green]Scientific Reasoning:[/bold green] {rec.scientific_reasoning}\n",
            f"[bold magenta]Connected Variables ({len(rec.connected_variables)}):[/bold magenta] {', '.join(rec.connected_variables)}\n",
            f"[bold yellow]Confidence Level:[/bold yellow] {rec.confidence_level * 100:.0f}%",
            f"[bold blue]Ecological Pathway:[/bold blue] {rec.ecological_pathway}\n",
        ]

        # Impacts Subtable
        table = Table(
            title=f"Projected Multi-Metric Impacts: {rec.title}", border_style="cyan"
        )
        table.add_column("Metric", style="bold white")
        table.add_column("Baseline", style="red")
        table.add_column("Projected Improvement", style="green")
        table.add_column("Time Horizon", style="cyan")
        table.add_column("Biogeochemical Mechanism", style="dim")

        for imp in rec.impacted_metrics:
            table.add_row(
                imp.metric_name,
                imp.baseline_estimate,
                imp.projected_improvement,
                imp.time_horizon.value,
                imp.mechanism,
            )

        console.print(
            Panel(
                "\n".join(rec_content),
                title=f"[bold white]{rec.title}[/bold white]",
                border_style="green",
            )
        )
        console.print(table)

        # Citations
        cites = [
            f"• [bold]{c.id}[/bold]: {c.title} ({c.publisher_or_journal}, {c.year}) - [dim]{c.doi_or_url}[/dim]"
            for c in rec.citations
        ]
        console.print(
            Panel(
                "\n".join(cites),
                title="Scientific Evidence & Citations",
                border_style="blue",
            )
        )


def run_interactive_chat() -> None:
    """Runs interactive multi-turn terminal conversation with memory and clarification."""
    console.print(
        Panel.fit(
            "[bold green]Darukaa.Earth Biodiversity Intelligence Chatbot[/bold green]\n"
            "[white]Type your environmental query or observation. Type 'exit' or 'quit' to stop.[/white]\n"
            "[dim]Try: 'Biodiversity is declining on my land' or provide full soil metrics.[/dim]",
            border_style="green",
        )
    )

    session_store = SessionStore()
    session = session_store.get_or_create("cli-interactive")
    extractor = ParameterExtractor()
    clarifier = ClarificationEngine()
    reasoner = EnvironmentalReasoner()

    while True:
        try:
            user_input = console.input("\n[bold green]User ❯ [/bold green]").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("[dim]Exiting Darukaa CLI. Goodbye![/dim]")
                break
            if user_input.lower() in ["reset", "clear"]:
                session = session_store.reset("cli-interactive")
                console.print("[dim]Session context cleared.[/dim]")
                continue

            # Update state
            session.accumulated_state, extracted = extractor.extract_from_text(
                session.accumulated_state, user_input
            )
            session.add_user_turn(user_input, extracted)

            if extracted:
                console.print(f"[dim]⚡ Extracted parameters: {extracted}[/dim]")

            # Completeness check
            clarification = clarifier.evaluate_completeness(session.accumulated_state)

            if clarification.is_incomplete:
                console.print("\n[bold cyan]Darukaa Scientist ❯[/bold cyan]")
                console.print(Markdown(clarification.system_response))
                if clarification.suggested_quick_replies:
                    console.print("\n[dim]Suggested inputs:[/dim]")
                    for qr in clarification.suggested_quick_replies:
                        console.print(f"  [cyan]›[/cyan] {qr}")
                session.add_assistant_turn(clarification.system_response)
            else:
                # Synthesize reasoning
                result = reasoner.analyze(session.accumulated_state)
                console.print(
                    "\n[bold cyan]Darukaa Scientist ❯[/bold cyan] [bold green]Multi-Metric Diagnosis Complete[/bold green]"
                )
                console.print(
                    f"[bold]Active Variables Analyzed ({result.active_variables_count}):[/bold] {', '.join(result.variable_connections)}"
                )

                for rec in result.recommendations:
                    console.print(
                        f"\n[bold yellow]► Recommendation:[/bold yellow] [bold white]{rec.title}[/bold white]"
                    )
                    console.print(f"  [bold]Action:[/bold] {rec.primary_action}")
                    console.print(f"  [bold]Reasoning:[/bold] {rec.scientific_reasoning}")
                    console.print(
                        f"  [bold]Pathway:[/bold] [dim]{rec.ecological_pathway}[/dim]"
                    )

                    table = Table(border_style="dim")
                    table.add_column("Metric", style="bold")
                    table.add_column("Projected Improvement", style="green")
                    table.add_column("Time Horizon", style="cyan")
                    for imp in rec.impacted_metrics:
                        table.add_row(
                            imp.metric_name,
                            imp.projected_improvement,
                            imp.time_horizon.value,
                        )
                    console.print(table)

                    console.print(
                        "  [dim]Authoritative Citations:[/dim] "
                        + ", ".join(f"[{c.id}] {c.title}" for c in rec.citations)
                    )

        except KeyboardInterrupt:
            console.print("\n[dim]Session interrupted. Exiting.[/dim]")
            break


def run_query_mode(query_text: str) -> None:
    """Queries the knowledge base directly."""
    retriever = KnowledgeRetriever()
    results = retriever.query(query_text, top_k=5)
    console.print(
        Panel.fit(
            f"[bold cyan]Retrievable Knowledge Layer - Query: '{query_text}'[/bold cyan]"
        )
    )
    for r in results:
        console.print(
            f"\n[bold green][Score: {r.relevance_score}] {r.title}[/bold green] (Domain: {r.domain})"
        )
        console.print(f"[dim]{r.matched_snippet}[/dim]")
        console.print(
            f"[bold]Citation:[/bold] {r.citation.id} - {r.citation.title} ({r.citation.publisher_or_journal}, {r.citation.year})"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Darukaa.Earth AI Biodiversity Intelligence CLI"
    )
    parser.add_argument(
        "mode", nargs="?", default="chat", choices=["chat", "benchmark", "query"]
    )
    parser.add_argument("--query", "-q", help="Query string for knowledge retrieval mode")
    parser.add_argument(
        "--analyze", "-a", help="JSON string of environmental metrics to analyze directly"
    )
    args = parser.parse_args()

    if args.analyze:
        try:
            data = json.loads(args.analyze)
            state = EnvironmentalState()
            extractor = ParameterExtractor()
            state = extractor.update_state_from_dict(state, data)
            reasoner = EnvironmentalReasoner()
            result = reasoner.analyze(state)
            console.print(result.model_dump_json(indent=2))
        except Exception as e:
            console.print(f"[red]Error analyzing input: {e}[/red]")
            sys.exit(1)
        return

    if args.mode == "benchmark":
        run_benchmark_mode()
    elif args.mode == "query":
        q = args.query or "soil organic carbon semi-arid"
        run_query_mode(q)
    else:
        run_interactive_chat()


if __name__ == "__main__":
    main()
