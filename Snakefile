from pathlib import Path
import csv
import os
import sys

PDF_PYTHON = os.environ.get("PDF_PYTHON", sys.executable)

rule all:
    input:
        'Potash_Infographic.pdf',
        'Potash_Infographic.png',
        'Potash_Explanation.pdf',
        'Potash_Infographic_R_Code.pdf',
        'Potash_Rights_and_Licensing.pdf'

rule check_inputs:
    input:
        'explanation.txt', 'references.tsv'
    output:
        'inputs_checked.txt'
    run:
        count = len(Path(input[0]).read_text().split())
        assert 300 <= count <= 500, f'Explanation has {count} words'
        with open(input[1]) as f:
            refs = list(csv.DictReader(f, delimiter='\t'))
        assert len(refs) >= 4
        Path(output[0]).write_text(f'{count} explanation words; {len(refs)} sources; inputs checked.\n')

rule render_in_R:
    input:
        'build.R'
    output:
        'Potash_Infographic.pdf',
        'Potash_Infographic.png'
    shell:
        'Rscript build.R'

rule build_explanation:
    input:
        'build_explanation.py', 'Acknowledgements.html', 'orcid.png', 'explanation.txt', 'references.tsv', 'inputs_checked.txt'
    output:
        'Potash_Explanation.pdf'
    params:
        python=PDF_PYTHON
    shell:
        '{params.python:q} build_explanation.py'

rule build_code_pdf:
    input:
        'build_code_pdf.py', 'build.R', 'orcid.png'
    output:
        'Potash_Infographic_R_Code.pdf'
    params:
        python=PDF_PYTHON
    shell:
        '{params.python:q} build_code_pdf.py'

rule build_rights:
    input:
        'build_rights.py', 'Rights_declaration.html', 'orcid.png'
    output:
        'Potash_Rights_and_Licensing.pdf'
    params:
        python=PDF_PYTHON
    shell:
        '{params.python:q} build_rights.py'
