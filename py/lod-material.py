__author__ = "Florian Thiery"
__copyright__ = "MIT Licence 2023, LEIZA, Florian Thiery"
__credits__ = ["Florian Thiery"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Florian Thiery"
__email__ = "florian.thiery@leiza.de"
__status__ = "beta"
__update__ = "2023-12-06"

# import dependencies
import uuid
import requests
import io
import pandas as pd
import os
import codecs
import datetime
import importlib
import sys
import hashlib
from pathlib import Path  # for file management


# set UTF8 as default
importlib.reload(sys)

# set starttime
starttime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
lines = []

# set paths I

file_name = "scherbe.csv"
dir_path = os.path.dirname(os.path.realpath(__file__))


def get_project_root() -> Path:
    return Path(__file__).parent.parent


Path = get_project_root()

# joinpath used to join parts of the path together. Path as project root
file_in = Path.joinpath("csv").joinpath(file_name)
url = "https://docs.google.com/spreadsheets/d/1jEBkurkQzwT0_SsBGKPod--AQuS6IOs0/export?gid=1590711087&format=csv"

# read csv file
data = pd.read_csv(
    url,
    encoding='utf-8',
    usecols=['id', 'label', 'type', 'nomisma', 'wikidata', 'gettyaat'],
    na_values=['.', '??', 'NULL']  # take any '.' or '??' values as NA
)
print("*****************************************")
print(data.info())

# create triples from dataframe
lineNo = 2
for index, row in data.iterrows():
    tmpno = lineNo - 2
    lineNo += 1

    # typing
    lines.append("isegrim:material_" +
                 str(row['id']) + " " + "rdf:type" + " skos:Concept .")
    # lines.append("isegrim:material_" +
    #             str(row['id']) + " " + "rdf:type" + " prov:Entity .")

    # metadata
    lines.append("isegrim:material_" +
                 str(row['id']) + " " + "skos:prefLabel" + " '" + str(row['label']) + "'@en.")
    if str(row['type']) != 'nan':
        lines.append("isegrim:material_" +
                     str(row['id']) + " " + "skosplus:type" + " '" + str(row['type']) + "'@en.")

    # alignments
    if str(row['nomisma']) != 'nan':
        lines.append("isegrim:material_" + str(row['id']) + " " +
                     "skos:closeMatch" + " <http://nomisma.org/id/" + str(row['nomisma']) + ">.")
    if str(row['wikidata']) != 'nan':
        lines.append("isegrim:material_" + str(row['id']) + " " +
                     "skos:closeMatch" + " <http://wikidata.org/entity/" + str(row['wikidata']) + ">.")
    if str(row['gettyaat']) != 'nan':
        lines.append("isegrim:material_" + str(row['id']) + " " +
                     "skos:closeMatch" + " <http://vocab.getty.edu/aat/" + str(int(row['gettyaat'])) + ">.")

    '''
    # license
    lines.append("bb5kbc:ic_" + str(row['id']) + " " + "dct:license" +
                 " <" + "https://creativecommons.org/licenses/by/4.0/" + "> .")
    lines.append("bb5kbc:ic_" + str(row['id']) + " " + "dct:creator" +
                 " <" + "https://orcid.org/0000-0002-3246-3531" + "> .")
    lines.append("bb5kbc:ic_" + str(row['id']) + " " + "dct:creator" +
                 " <" + "https://orcid.org/0000-0003-4696-2101" + "> .")
    lines.append("bb5kbc:ic_" + str(row['id']) + " " + "dct:rightsHolder" +
                 " <" + "https://orcid.org/0000-0002-3246-3531" + "> .")
    lines.append("bb5kbc:ic_" + str(row['id']) + " " + "dct:rightsHolder" +
                 " <" + "https://orcid.org/0000-0003-4696-2101" + "> .")

    # prov-o for script
    lines.append("bb5kbc:ic_" + str(row['id']) + " " +
                 "prov:wasAttributedTo" + " <https://github.com/Research-Squirrel-Engineers/bb-5kbc/blob/main/py/scherbe.py> .")
    lines.append("bb5kbc:ic_" + str(row['id']) + " " +
                 "prov:wasDerivedFrom" + " <https://github.com/Research-Squirrel-Engineers/bb-5kbc> .")
    lines.append("bb5kbc:ic_" + str(row['id']) + " " +
                 "prov:wasGeneratedBy" + " bb5kbc:ic_" + str(row['id']) + "_pyscript .")
    lines.append("bb5kbc:ic_" +
                 str(row['id']) + "_pyscript " + "rdf:type" + " <http://www.w3.org/ns/prov#Activity> .")
    lines.append("bb5kbc:ic_" +
                 str(row['id']) + "_pyscript " + "prov:startedAtTime '" + starttime + "'^^xsd:dateTime .")
    lines.append("bb5kbc:ic_" +
                 str(row['id']) + "_pyscript " + "prov:endedAtTime '" +
                 datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ") + "'^^xsd:dateTime .")
    lines.append("bb5kbc:ic_" +
                 str(row['id']) + "_pyscript " + "prov:wasAssociatedWith" + " <https://github.com/Research-Squirrel-Engineers/bb-5kbc/blob/main/py/scherbe.py> .")
    '''

    lines.append("")

files = (len(lines) / 100000) + 1
print("triples", len(lines), "files", int(files))
thiscount = len(lines)

# write output files
f = 0
step = 100000
prefixes = ""
prefixes += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\r\n"
prefixes += "@prefix owl: <http://www.w3.org/2002/07/owl#> .\r\n"
prefixes += "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\r\n"
prefixes += "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\r\n"
prefixes += "@prefix geosparql: <http://www.opengis.net/ont/geosparql#> .\r\n"
prefixes += "@prefix dc: <http://purl.org/dc/elements/1.1/> .\r\n"
prefixes += "@prefix dct: <http://purl.org/dc/terms/> .\r\n"
prefixes += "@prefix sf: <http://www.opengis.net/ont/sf#> .\r\n"
prefixes += "@prefix prov: <http://www.w3.org/ns/prov#> .\r\n"
prefixes += "@prefix foaf: <http://xmlns.com/foaf/0.1/> .\r\n"
prefixes += "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\r\n"
prefixes += "@prefix pleiades: <https://pleiades.stoa.org/places/vocab#> .\r\n"
prefixes += "@prefix wikidata: <http://wikidata.org/entity/> .\r\n"
prefixes += "@prefix lado: <http://archaeology.link/ontology#> .\r\n"
prefixes += "@prefix isegrim: <http://data.archaeology.link/data/isegrim/> .\r\n"
prefixes += "@prefix skosplus: <http://ontology.skosplus.net/> .\r\n"
prefixes += "@prefix fsl: <http://archaeoinformatics.link/ontology#> .\r\n"
prefixes += "@prefix fsld: <http://fuzzy-sl.squirrel.link/data/> .\r\n"
prefixes += "\r\n"

for x in range(1, int(files) + 1):
    strX = str(x)
    filename = Path.joinpath("rdf").joinpath("material.ttl")
    file = codecs.open(filename, "w", "utf-8")
    file.write(
        "# create triples from https://github.com/nfdi4objects/isegrim \r\n")
    file.write(
        "# on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\r\n\r\n")
    file.write(prefixes)
    i = f
    for i, line in enumerate(lines):
        if (i > f - 1 and i < f + step):
            file.write(line)
            file.write("\r\n")
    f = f + step
    print(" > material.ttl")
    file.close()

print("*****************************************")
print("SUCCESS: closing script")
print("*****************************************")
