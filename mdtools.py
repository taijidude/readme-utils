from dataclasses import dataclass
from pathlib import Path
import enum
import textwrap

class NoSectionException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message) 

class SectionType(enum.Enum):
    description = '# Description'
    todo = '# Todos'
    problem = '# Problems'

class Section():
    """
    Teil eines Markdown Documents
    """
    def __init__(self, name: str, lines: list[str]):
        self.name = name
        self.lines = lines
        self.sectionType = self.getSectionType(name)
        
    def getSectionType(self, name: str) -> SectionType: 
        if name.startswith(SectionType.todo.value):
            return SectionType.todo
        elif name.startswith(SectionType.problem.value):
            return SectionType.problem
        elif name.startswith(SectionType.description.value):
            return SectionType.description


    def __str__(self):
        joinedLines: str = '\n'.join(self.lines)
        return textwrap.dedent(f"""\
        {self.name}
        {joinedLines}
        """)

class Document(): 
    """
    Stellt ein komplettes Markdown Document dar. 
    Besteht im wesentlichen aus einer List von Sections
    """

    def __init__(self,sections: list[Section]):
        self.sections = sections
    
    def hasSections(self) -> bool:
        return len(self.sections) > 0

    def hasProblemSection(self) -> bool:
        return len([section for section in self.sections if section.sectionType is SectionType.problem]) == 1

    def hasTodoSection(self) -> bool: 
        return len([section for section in self.sections if section.sectionType is SectionType.todo]) == 1

    @property
    def titleSection(self) -> Section:
        ps: Section = self.problemSection
        ts: Section = self.todoSection
        ds: Section = self.descriptionSection
        return [section for section in self.sections if section.sectionType not in [ps, ts, ds]][0]


    @property
    def problemSection(self) -> Section:
        return [section for section in self.sections if section.sectionType is SectionType.problem][0]

    @property
    def todoSection(self) -> Section:
        return [section for section in self.sections if section.sectionType is SectionType.todo][0]
    
    @property
    def descriptionSection(self) -> Section:
        return [section for section in self.sections if section.sectionType is SectionType.description][0]

    def validate(self): 
        if len([s for s in self.sections if s.sectionType is SectionType.todo]) == 0:
            raise NoTodoSectionError
    
        if len([s for s in self.sections if s.sectionType is SectionType.problem]) == 0:
            raise NoProblemSectionError

    def addProblem(self, description: str):
        self.problemSection.lines.append(f"- {description}")

    def addTodo(self, description: str):
        self.todoSection.lines.append(f"- {description}")

    def __str__(self):
        return textwrap.dedent(f"""\
        {self.titleSection}""")

    # def __str__(self):
    #     return textwrap.dedent(f"""\
    #     {self.titleSection}
    #     {self.descriptionSection}
    #     {self.todoSection}
    #     {self.problemSection}""")

    def writeTo(self, target: Path): 
        pass

NoTodoSectionError = NoSectionException(message="Keine Todo Section gefunden")
NoProblemSectionError = NoSectionException(message="Keine Problem Section gefunden")

def parseDocument(toParse: Path) -> Document: 
    sections: list[Section] = []
    with open(toParse, mode="r") as file:
        lines = file.readlines()
        currentSection: Section = None
        for line in lines: 
            # Hier sollte der Typ der Zeile geprüft werden
            line = line.strip()
            if line.startswith('#'):
                currentSection = Section(name=line, lines=[])
                sections.append(currentSection)
            else:
                currentSection.lines.append(line)
    return Document(sections)

