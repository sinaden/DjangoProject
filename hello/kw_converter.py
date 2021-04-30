import pandas
import xml.etree.cElementTree as ET
#from django.contrib.staticfiles.storage import staticfiles_storage

# Subset & features converter to xml
class KWConverter():   
    def __init__(self, name):
        xml_file = ET.parse("assets/keyword_definitions_template.xml")

        self.main_root = xml_file.getroot()
        self.name = name
    
    def keyword_to_xml(self, a):
        sfd = self.main_root.find("Keywords_Dataset")
        no_k = len(list(sfd)) # number of keywords already in the tree
        no_k += 1
        subset_element = ET.Element("Keyword_"+str(no_k))
        
        for tag, answer in a.items():
            new_element = ET.Element(tag)
            new_element.text = answer
            subset_element.append(new_element)
        sfd.append(subset_element)


    def indent(self,elem, level=0):
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    
    def save(self):
        tree = ET.ElementTree(self.main_root)
        self.indent(self.main_root)
        file_name = "keyword_definitions.xml".format(title = self.name)
        tree.write("assets\\" + file_name, encoding="utf-8")
        return file_name