from vehicle_data import VehicleDataFetcher
from date_gen import DateGenerator
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.prompt import Prompt
from rich.align import Align
import time
import json

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"request_delay": 3.0, "retry_delay": 15.0, "max_retries": 3, "timeout": 15}

def run_console_ui() -> None:
    try:
        config = load_config()
        console = Console()

        console.print(Panel(Align.center("[bold]Wyszukiwanie daty pierwszej rejestracji[/]"), border_style="cyan", title="Historia Pojazdu"))

        reg_num = Prompt.ask("Podaj numer rejestracyjny (np. PKS66111)").strip().upper()
        vin_num = Prompt.ask("Podaj numer VIN (np. VF1RJB00265666700)").strip().upper()
        years_input = Prompt.ask("Podaj rok lub lata po przecinku (np. 2020, 2021)")

        years_to_check = [int(y.strip()) for y in years_input.split(",") if y.strip().isdigit()]

        if not years_to_check:
            console.print("[bold red]Błąd: Nie podano żadnego poprawnego roku![/]")
            return
        
        found_date = None
        fetcher = VehicleDataFetcher()

        for year in years_to_check:
            if found_date:
                break
                
            date_generator = DateGenerator(year)
            total_days = (date_generator.end_date - date_generator.start_date).days + 1
            
            progress_cols = [SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), 
                            TextColumn("{task.completed}/{task.total}"), TimeElapsedColumn(), TimeRemainingColumn()]

            with Progress(*progress_cols, expand=True) as progress:
                task_id = progress.add_task(f"Przeszukiwanie {year}...", total=total_days)
                
                for current_date in date_generator:
                    success = False
                    attempts = 0
                    
                    while not success and attempts < config['max_retries']:
                        try:
                            progress.update(task_id, description=f"Sprawdzanie {current_date}")
                            response = fetcher.get_vehicle_data(reg_num, vin_num, current_date, timeout=config['timeout'])

                            if response.status_code == 200:
                                found_date = current_date
                                success = True
                                progress.console.print(f"[bold green]SUKCES![/] Znaleziono datę: {current_date}")
                            elif response.status_code == 429:
                                wait = config['retry_delay'] * (attempts + 1)
                                progress.console.print(f"[yellow]Limit 429! Czekam {wait}s...[/]")
                                time.sleep(wait)
                                fetcher = VehicleDataFetcher()
                                attempts += 1
                            elif response.status_code == 404:
                                success = True
                                time.sleep(config['request_delay'])
                            else:
                                progress.console.print(f"[red]Błąd {response.status_code} dla {current_date}. Ponawiam...[/]")
                                time.sleep(config['request_delay'])
                                attempts += 1

                        except Exception as e:
                            attempts += 1
                            progress.console.print(f"[bold red]Błąd połączenia ({attempts}/{config['max_retries']}): {e}[/]")
                            time.sleep(config['retry_delay'])
                            fetcher = VehicleDataFetcher()

                    progress.advance(task_id)
                    if found_date:
                        break

        if found_date:
            console.print(Panel(f"[bold green]Data pierwszej rejestracji to: {found_date}[/]", title="WYNIK", border_style="green"))
        else:
            console.print(Panel("[bold red]Nie znaleziono daty w żadnym z podanych lat.[/]", title="WYNIK", border_style="red"))

    except KeyboardInterrupt:
        print("")
        console.print(Panel("[bold red]Działanie przerwane (Ctrl+C).[/]", border_style="red"))

if __name__ == "__main__":
    run_console_ui()