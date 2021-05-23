import pandas
import xml.etree.cElementTree as ET
#from django.contrib.staticfiles.storage import staticfiles_storage

# Subset & features converter to xml
class SFConverter():   
    def __init__(self, name):
        #url = staticfiles_storage.url('purpose_ethics.xml')
        xml_file = ET.parse("assets/feature_description_cleaned.xml")

        self.main_root = xml_file.getroot()
        self.name = name
    
    def subset_to_xml(self, a):
        if a['ID'] == None or a['ID'] == '':
            raise Exception(" One of the subsets does not have an ID")
        sfd = self.main_root.find("Subset_Feature_Dataset")

        subset_element = ET.Element("Subset_"+a["ID"])
        for tag, answer in a.items():
            new_element = ET.Element(tag)
            new_element.text = answer
            subset_element.append(new_element)
            
        f = ET.Element("Features")
        subset_element.append(f)
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

    def feature_to_xml(self, a): 
        if a['ID'] == None or a['ID'] == '':
            raise Exception(" One of the features does not have an ID")
        sfd = self.main_root.find("Subset_Feature_Dataset")
        
        subset = sfd.find("Subset_"+a["Subset"])
        
        if subset == None:
            raise Exception("Feature {my_id} is not child to an existing subset. ".format(my_id = a['ID'] ))
        features = subset.find("Features")
        if subset == None:
            print("No subset found")
            return None
        no_f = len(list(features))
        no_f += 1
        feature_element = ET.Element("Feature_"+ str(no_f))

        for tag, answer in a.items():
            new_element = ET.Element(tag)
            new_element.text = answer
            feature_element.append(new_element)
            
        features.append(feature_element)

    def validate_structure(self):
        q = self.main_root.find("Subset_Feature_Dataset")
        subs = list(q)
        print("should type the categories") 
        items_pattern = ["ID", "Name", "LastUpdate", "Modality", "Format", "Size",
                        "ParentID", "Purpose","Link","Covmat","Modsys","Features"]
        numsubs = len(subs)
        print(subs)
        for i in range(0, numsubs):
            if subs[i].tag != "Subset_" + str(i + 1):
                return "Subset ID Error"
            items = list(subs[i])
            for j in range(0,len(items)):
                if items_pattern[j] != items[j].tag:
                    return "Structure Validation Error"
        return "Valid"

    def save(self):
        result = self.validate_structure()
        if result != "Valid":
            return result

        tree = ET.ElementTree(self.main_root)
        self.indent(self.main_root)
        file_name = "feature_description.xml".format(title = self.name)
        tree.write("assets\\" + file_name, encoding="utf-8")
        return file_name