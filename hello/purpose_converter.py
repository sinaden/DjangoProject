import pandas
import xml.etree.cElementTree as ET


class PurposeConverter():   
    def __init__(self, name):
        #url = staticfiles_storage.url('purpose_ethics.xml')
        xml_file = ET.parse("assets/purpose_ethics.xml")

        self.main_root = xml_file.getroot()
        self.name = name

    def form_xml(self, key, value):
        q = self.main_root.find("questionnaire")
        cat_map = {"motivation":"category_1","composition":"category_2","collectionprocess":"category_3",
                "pcl":"category_4","uses":"category_5","distribution":"category_6", "maintenance":"category_7"}
        
        cat_, ans_ = key.split("_")
        ans = int(ans_) -1 
        
        cat = cat_map[cat_] 

        c_tag = q.find(cat)
        a_tag = c_tag.find("answers")
        answer = a_tag.find("A"+str(ans))
        answer.text = value

    
    def validate_structure(self):
        q = self.main_root.find("questionnaire")
        cats = list(q)
        print("should type the categories") 
        items_pattern = ["name", "code", "description", "questions", "messages", "answers"]
        cnt = 1
        for cat in cats:
            if cat.tag != "category_"+str(cnt):
                return False
            cnt += 1
            items = list(cat) 
            for i in range(0,len(items)):
                if items_pattern[i] != items[i].tag:
                    return False

        return True
    def save(self):
        result = self.validate_structure()
        if not result:
            return "Structure Validation Error"
        tree = ET.ElementTree(self.main_root)
        file_name = "questionnaire.xml".format(title = "self.name")
        tree.write("assets\\" + file_name)
        return file_name