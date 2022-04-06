import sys
import xml.etree.ElementTree as ET
from inspect import getmembers, isclass, isfunction

tree = ET.parse(sys.argv[1])
root = tree.getroot()

print(sys.argv)
# case_information = root.findall('{*}caseInformation') #Verweis auf die Falldaten
# source_extraction = root.findall('{*}sourceExtractions') #Verweis auf die Übersicht der Auslesungen
# extraction_data = root.findall('{*}metadata') #Verweis auf die Inhaltsdaten der Auslesungen

# anzahl = len(root.findall("{*}sourceExtractions/{*}extractionInfo")) #Anzahl der Auslesungen ermitteln

def additional_fields_ausgeben():
    generator_additional_fields = root.iterfind("{*}metadata/[@section = 'Additional Fields']/{*}item")
    while True:
        item = next(generator_additional_fields, 'e')
        if (item == 'e'):
            break
        print(item.attrib['name'], ":", item.text)


def case_info_ausgeben():
    generator_case_info = root.iterfind("{*}caseInformation/{*}field")

    while True:
        item = next(generator_case_info, 'e')
        if (item == 'e'):
            break
        print(item.attrib['name'], ":", item.text)


def extraction_data_ausgeben(i):
    generator_extraction_data = root.iterfind(
        "{*}metadata/[@section = 'Extraction Data']/{*}item/[@sourceExtraction = '" + str(i) + "']")
    while True:
        item = next(generator_extraction_data, 'e')
        if (item == 'e'):
            break
        print("\t", item.attrib['name'], ":", item.text)


def chatprogramme_ausgeben():
    generator_chatprogramme = root.iterfind(
        "{*}decodedData/{*}modelType/{*}model/[@type='Chat']/{*}field/[@name = 'Source']/{*}value")
    chatprogramme = set()
    chatprogramme.clear
    while True:
        item = next(generator_chatprogramme, 'e')
        if (item == 'e'):
            break
        chatprogramme.add(item.text)
    # Als Liste übergeben, sortieren und ausgeben
    chatprogramme_lst = list(chatprogramme)
    chatprogramme_lst.sort()
    for chatprogramm in chatprogramme_lst:
        print(chatprogramm)


def gesamt_bericht_ausgeben():
    # Ausgabe gesamt sortiert

    # Fallinformationen
    print("Fallinformationen:")
    case_info_ausgeben()
    print("\n")
    print("Programmversion:")
    additional_fields_ausgeben()
    print("\n")
    print("Folgende Chat-Programme konnten ausgelesen werden:")
    chatprogramme_ausgeben()
    print("\n")
    print("Detailierte Informationen zu den einzelnen Auslesungen:\n")
    generator_source_extractions = root.iterfind("{*}sourceExtractions/{*}extractionInfo")
    while True:
        item = next(generator_source_extractions, 'e')
        if (item == 'e'):
            break
        print("Auslesung Nr:", item.attrib['id'], ", Art:", item.attrib['name'])
        extraction_data_ausgeben(item.attrib['id'])


gesamt_bericht_ausgeben()