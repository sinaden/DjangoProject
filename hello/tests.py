# from django.contrib.auth.models import AnonymousUser, User
# from django.test import TestCase, RequestFactory

# from .views import index


# class SimpleTest(TestCase):
#     def setUp(self):
#         # Every test needs access to the request factory.
#         self.factory = RequestFactory()

#     # def test_details(self):
#     #     # Create an instance of a GET request.
#     #     request = self.factory.get("/")
#     #     request.user = AnonymousUser()

#     #     # Test my_view() as if it were deployed at /customer/details
#     #     response = index(request)
#     #     self.assertEqual(response.status_code, 200)
#     def test_testhomepage(self):
#         response = self.client.get("/")
#         self.assertEqual(response.status_code,200)

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver import ActionChains

from selenium.webdriver.common.by import By



# class Hosttest(LiveServerTestCase):
  	
# 	def testhomepage(self):
# 		driver = webdriver.Chrome()
# 		# try driver = webdriver.Chrome('./chromedriver') with the driver in the project folder if you cant set to path

# 		driver.get('http://127.0.0.1:5000/')
# 		# try driver.get(self.live_server_url) if driver.get('http://127.0.0.1:8000/') does not work
		
# 		assert "Maids" in driver.title

    # def testlogin(self):
	# 	driver = webdriver.Chrome()
	# 	# try driver = webdriver.Chrome('./chromedriver') with the driver in the project folder if you cant set to path

	# 	driver.get('http://127.0.0.1:5000/')
	# 	# try driver.get(self.live_server_url) if driver.get('http://127.0.0.1:8000/') does not work
		
	# 	assert "Maids" in driver.title


class LoginFormTest(LiveServerTestCase):


    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get('http://maidsform.herokuapp.com/login/')

        user_name = self.browser.find_element_by_name('username')
        user_password = self.browser.find_element_by_name('password')

        #time.sleep(3)

        submit = self.browser.find_element_by_xpath('/html/body/div[1]/div/div/form/button')

        user_name.send_keys('sina')
        user_password.send_keys('Sinaden1376')

        submit.send_keys(Keys.RETURN)

        
        #time.sleep(30)



    def testform(self):
        #driver = webdriver.Chrome()

        self.browser.get('http://maidsform.herokuapp.com/owned/')

        #time.sleep(1)
        #self.browser.find_element(By.xpath("(//div[@class='panel-heading'])[6]/a")).click()
        showbtn = self.browser.find_element_by_xpath("//*[@id=\"owned_repos_container\"]/div[1]/div/div/div[1]/h3/a").get_attribute('href')

        print(showbtn)

        #time.sleep(1)
        self.browser.get(showbtn)

        #time.sleep(30)
        assert 'Medical AI Datasheet (MAIDS)' in self.browser.title

    # def testeditcontext(self):
    #     self.browser.get('http://127.0.0.1:5000/owned/')
        
    #     self.browser.find_element_by_xpath("//*[@id=\"owned_repos_container\"]/div[1]/div/div/div[2]/div/a[1]").click()
        
    #     title = self.browser.find_element_by_id('id_title')
    #     authors = self.browser.find_element_by_id('id_authors')
    #     abstract = self.browser.find_element_by_id('id_abstract')
    #     research_main = self.browser.find_element_by_id('id_research_main')
    #     research_secondary = self.browser.find_element_by_id('id_research_secondary')

    #     title.clear()
    #     title.send_keys('')
    #     authors.clear()
    #     authors.send_keys('Test1, Test2')
    #     abstract.send_keys('')
    #     research_main.send_keys('')
    #     research_secondary.send_keys('')


    #     submit = self.browser.find_element_by_xpath('/html/body/div/div[1]/div/form/button')
    #     submit.click()

    #     time.sleep(3)

    #     validation_message1 = title.get_attribute("validationMessage")
    #     #validation_message2 = authors.get_attribute("validationMessage")

        
    #     self.assertEqual(validation_message1,"Please fill out this field.")

    #     title.send_keys('Test Title')
    #     submit.click()

    #     assert  "Successfully Edited" in self.browser.page_source








