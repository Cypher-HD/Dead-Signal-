# engine/livehud.py
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich import box
from time import sleep
from engine.statuswatch import get_status_summary
from engine.trafficwatch import get_current_pps
from engine.netheatmap import get_heatmap_visual
from engine.portscan import get_open_ports

def generate_dashboard(target):
    # Safe access
    summary = get_status_summary() or {}
    pps = get_current_pps() or 0
    heatmap = get_heatmap_visual() or "..."

    status = summary.get("last_status")
    status_str = "UP" if status else ("DOWN" if status is False else "...")
    latency = summary.get("last_latency")
    latency_str = f"{latency} ms" if latency else "N/A"
    score = summary.get("threat_score")
    score_str = f"{score}/100" if score is not None else "..."

    # Table initialization
    table = Table.grid(expand=True)
    table.add_column(justify="center", ratio=1)
    table.add_row(f"[bold magenta]:: DEAD SIGNAL // TARGET: {target}[/bold magenta]")

    table.add_row(Panel.fit(
        f"[green]Status:[/green] {status_str}   "
        f"[yellow]Latency:[/yellow] {latency_str}   "
        f"[red]Threat Score:[/red] {score_str}   "
        f"[cyan]Traffic:[/cyan] {pps} PPS",
        box=box.ROUNDED,
        border_style="cyan"
    ))

    table.add_row(Panel.fit(
        heatmap,
        title="Network Heatmap",
        box=box.MINIMAL_DOUBLE_HEAD,
        border_style="magenta"
    ))

    open_ports = get_open_ports()
    port_str = ", ".join([str(p) for p in open_ports]) if open_ports else "..."
    table.add_row(Panel.fit(
        f"[green]Open TCP Ports:[/green] {port_str}",
        box=box.SQUARE,
        border_style="red"
    ))

    return table

def run_live_display(target):
    with Live(refresh_per_second=1) as live:
        while True:
            try:
                live.update(generate_dashboard(target))
                sleep(1)
            except Exception as e:
                live.update(Panel.fit(f"[ERROR] {str(e)}", border_style="bold red"))
                sleep(1)
