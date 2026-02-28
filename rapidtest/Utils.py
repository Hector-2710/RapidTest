from typing import Any, Optional
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.json import JSON
from rich.text import Text
from rich import box
import traceback

console = Console()

def print_report(result: str, url: str, status: int, body: Any, error_msg: Optional[str] = None) -> None:
    """
    Imprime un reporte visual de alta calidad del resultado de una prueba en la consola
    utilizando la librería 'rich'. Soporta layouts responsivos para consolas pequeñas.

    Args:
        result (str): El resultado de la prueba ('PASSED' o 'FAILED').
        url (str): La URL a la que se realizó la petición.
        status (int): El código de estado HTTP recibido.
        body (any): El cuerpo de la respuesta (usualmente un dict o list).
        error_msg (str, optional): Mensaje detallado del error si la prueba falló.
    """
    
    # Sensibilidad al ancho de la consola
    width = console.width
    is_narrow = width < 60
    
    # Configuración de colores y estilo según el resultado
    if result == "PASSED":
        main_color = "spring_green3"
        header_style = "bold white on spring_green3"
        border_style = "spring_green3"
        icon = "✅"
    else:
        main_color = "bright_red"
        header_style = "bold white on bright_red"
        border_style = "bright_red"
        icon = "❌"

    # Encabezado principal (más corto si es estrecho)
    title_text = f" {icon} {result} " if is_narrow else f" {icon} TEST {result} "
    header_text = Text(title_text, style=header_style)
    
    # Tabla de metadatos (optimizada para espacio)
    metadata_table = Table(show_header=False, box=None, padding=(0, 1 if is_narrow else 2))
    metadata_table.add_row(Text("URL:", style="bold cyan"), Text(url, overflow="fold"))
    
    # Status color logic
    status_style = "bold green" if 200 <= status < 300 else "bold yellow" if status >= 400 else "bold red"
    metadata_table.add_row(Text("Status:", style="bold cyan"), Text(str(status), style=status_style))

    # Construcción del reporte
    console.print("") # Espacio inicial
    
    # Panel principal
    content = []
    content.append(metadata_table)
    
    if error_msg:
        content.append(Panel(
            Text(error_msg, style="bold white"), 
            title="[bold white]Error[/]" if is_narrow else "[bold white]Error Detail[/]", 
            border_style="bright_red", 
            box=box.ROUNDED,
            padding=(0, 1)
        ))

    if body:
        # Si el body es un dict o list, usamos rich.json.JSON
        if isinstance(body, (dict, list)):
            json_renderable = JSON.from_data(body)
            content.append(Panel(
                json_renderable, 
                title="[bold cyan]Body[/]" if is_narrow else "[bold cyan]Response Body[/]", 
                border_style="cyan", 
                box=box.ROUNDED, 
                expand=True if is_narrow else False,
                padding=(0, 1) if is_narrow else (1, 2)
            ))
        else:
            content.append(Panel(
                str(body), 
                title="[bold cyan]Body[/]" if is_narrow else "[bold cyan]Response Body[/]", 
                border_style="cyan", 
                box=box.ROUNDED,
                padding=(0, 1)
            ))

    # Renderizamos todo dentro de un panel contenedor con bordes pesados
    # Usamos padding dinámico según el ancho
    main_panel = Panel(
        Group(*content),
        title=header_text,
        border_style=border_style,
        box=box.HEAVY_EDGE,
        padding=(0, 1) if is_narrow else (1, 2)
    )
    
    console.print(main_panel)
    console.print("") # Espacio final


def show_connection_error(url: str, exception: Exception) -> None:
    """
    Muestra un error de conexión detallado usando Rich.
    
    Args:
        url (str): La URL que falló
        exception (Exception): La excepción que ocurrió
    """
    error_text = Text()
    error_text.append("🔥 CRITICAL API ERROR\n", style="bold red")
    error_text.append(f"URL: ", style="bold")
    error_text.append(f"{url}\n", style="blue underline")
    error_text.append(f"Error Type: ", style="bold")
    error_text.append(f"{type(exception).__name__}\n", style="yellow")
    error_text.append(f"Error Message: ", style="bold")
    error_text.append(f"{str(exception)}\n", style="red")
    
    if hasattr(exception, 'response') and exception.response is not None:
        error_text.append(f"\nHTTP Status: ", style="bold")
        error_text.append(f"{exception.response.status_code}\n", style="red bold")
        error_text.append(f"Response Headers: ", style="bold")
        error_text.append(f"{dict(exception.response.headers)}\n", style="dim")
    
    panel = Panel(
        error_text,
        title="[bold red]❌ API CONNECTION FAILED[/bold red]",
        border_style="red",
        expand=False
    )
    
    console.print(panel)