import typer
from mdtools import parseDocument, Document
from pathlib import Path

app = typer.Typer()

@app.command()
def add():
    print("Projekt hinzufügen")

@app.command()
def list():
    print("Alle Projekte auflisten")

@app.command()
def delete():
    print("Projekt löschen")

@app.command()
def todo(text: str):
    doc: Document = parseDocument(Path("README.md"))    
    doc.addTodo(text)
    print("todo ergänzt")

@app.command()
def problem():
    print("problem ergänzt")


if __name__ == "__main__":
    app()