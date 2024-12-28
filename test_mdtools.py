import pytest, textwrap
from mdtools import *

def test_parseDocument(): 
    
    doc: Document = parseDocument(Path("README.md"))
    assert doc.hasSections() 
    assert len([item for item in doc.sections if not item.name.startswith("#")]) == 0    


def test_validateDocument():
    
    doc: Document = Document(sections=[])
    with pytest.raises(NoSectionException) as err:
        doc.validate()
        
    assert type(err.type) is type(NoSectionException)
    assert err.value.message == NoTodoSectionError.message
    doc.sections.append(Section(name='# Todos', lines=['- Example Todo']))
    with pytest.raises(NoSectionException) as err:
        doc.validate()
        
    assert type(err.type) is type(NoSectionException)
    assert err.value.message == NoProblemSectionError.message
    doc.sections.append(Section(name='# Problems', lines=['- Example Problem']))
    doc.validate()

def test_addProblem():
    sections: list[Section] = [
        Section(name='# Todos', lines=['- Example Todo']),
        Section(name='# Problems', lines=['- Example Problem']) 
    ]
    doc: Document = Document(sections)
    doc.addProblem(description='das ist ein neues Problem')
    assert '- das ist ein neues Problem' in doc.problemSection.lines 

def test_addTodo():
    sections: list[Section] = [
        Section(name='# Todos', lines=['- Example Todo']),
        Section(name='# Problems', lines=['- Example Problem']) 
    ]
    doc: Document = Document(sections)
    doc.addTodo(description='das ist ein neues Problem')
    assert '- das ist ein neues Problem' in doc.todoSection.lines

def test_SectionToString():
    section: Section = Section(name='# Description', lines=['testDiscription'])
    expected: str = textwrap.dedent("""\
    # Description
    testDiscription
    """)
    assert expected == section.__str__()

def test_DescriptionSection():
    sections: list[Section] = [
        Section(name='# Testproject', lines=['testSummary']),
        Section(name='# Description', lines=['Description how the tool works']),
        Section(name='# Todos', lines=['- Example Todo']),
        Section(name='# Problems', lines=['- Example Problem']) 
    ]
    doc: Document = Document(sections)
    assert doc.descriptionSection is not None



def test_DocumentToString():
    sections: list[Section] = [
        Section(name='# Testproject', lines=['testSummary'])
        #Section(name='# Description', lines=['Description how the tool works']),
        #Section(name='# Todos', lines=['- Example Todo']),
        #Section(name='# Problems', lines=['- Example Problem']) 
    ]
    doc: Document = Document(sections)
    assert len(doc.__str__()) != 0
    # expectedMdContent: str = textwrap.dedent("""\
    # # Testproject
    # testSummary
    # # Description
    # Description how the tool works    
    # # Todos
    # - Example Todo
    # # Problems
    # - Example Problem
    # """)

    expectedMdContent: str = textwrap.dedent("""\
    # # Testproject
    testSummary
     """)

    assert expectedMdContent == doc.__str__()





# def test_addWrite():
#     sections: list[Section] = [
#         Section(name='# Todos', lines=['- Example Todo']),
#         Section(name='# Problems', lines=['- Example Problem']) 
#     ]
#     doc: Document = Document(sections)
#     test_output: Path = Path('test.md')
#     doc.writeTo(test_output)
#     assert test_output.exists()
