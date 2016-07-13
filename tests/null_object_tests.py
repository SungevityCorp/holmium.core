import unittest
import time
from StdSuites import anything


from  holmium.core import Page, Element, Locators
from holmium.core.pageobject import NonexistentElement
from tests.utils import get_driver, make_temp_page
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, WebDriverException
from selenium.common.exceptions import TimeoutException, NoSuchFrameException
import hiro



class ElementTest(unittest.TestCase):
    page_content = """
            <body>
                <div id="simple_id">simple_id</div>
                <div id="other_id">simple_id</div>
                <div id="another_id">another_id</div>
                <div class="simple_class">simple_class</div>
                <div class="simple_class">simple_other_class</div>
                <div class="simple_xpath"><h3>Simple XPATH</h3></div>
            </body>
        """

    def setUp(self):
        self.driver = get_driver()




    def test_non_existence_eq_element(self):
        """test object equivalence test that expected parameters are displayed"""
        class SimplePage(Page):
            invalid_el = Element(Locators.ID, "foo")

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)

        non_exist_el = NonexistentElement()
        assert page.invalid_el == non_exist_el, "Expected object equivalence to evaluate TRUE"
        assert page.invalid_el.locator_type != non_exist_el.locator_type, "Expected different locator types"

    def test_non_existence_nq_element(self):
        """test object nonequivalence test that expected parameters are displayed"""
        class SimplePage(Page):
            class_el = Element(Locators.CLASS_NAME, "simple_class")
            class_xpath_el = Element(Locators.CLASS_NAME, "simple_xpath")

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
        non_exist_el = NonexistentElement()
        assert page != non_exist_el, "Expected SimplePage() and NonexistentElement != to evaluate FALSE"

    def test_non_existence_str_element(self):
        """test when str() is called on the object test that expected parameters are displayed"""
        class SimplePage(Page):
            class_el = Element(Locators.CLASS_NAME, "simple_class")
            exception_msg = "Class Name Found"
            query_string = "key1=value1&key2=value2"

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)

        result = NonexistentElement(page.exception_msg,page.class_el.text,page.query_string)

        test_str = str(result)
        assert test_str == format(result) , " Expected object format and str value are same"
        assert page.exception_msg in test_str
        assert page.class_el.text in test_str
        assert page.query_string in test_str

    def test_non_existence_repr_element(self):
        """when repr() is called on the object test that expected parameters can be referenced by name.
        (e.g: object.prop1, object.prop2 etc...)"""

        class SimplePage(Page):
            class_el = Element(Locators.CLASS_NAME, "simple_class")
            exception_msg = "Class Name Found"
            query_string = "key1=value1&key2=value2"

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
        non_exist_el = NonexistentElement()

        result = NonexistentElement(page.exception_msg, page.class_el.text, page.query_string)
        test_repr = repr(result)
        assert page.exception_msg in test_repr
        assert page.class_el.text in test_repr
        assert page.query_string in test_repr

    def test_non_existence_getAttr_element(self):
        """test that if an undefined property is referenced, an Exception is thrown that includes the initialization data
        #properties, (exception_class_name, locator_type, query_string)"""
        class SimplePage(Page):
            class_el = Element(Locators.CLASS_NAME, "simple_class")
            exception_msg = "Class Name Found"
            query_string = "key1=value1&key2=value2"
            invalid_el = Element(Locators.ID, "blargh")

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)
        non_exist_el = NonexistentElement(page.exception_msg, page.class_el.text, page.query_string)
        try:
            bar = non_exist_el.foo
        except Exception as e:
            assert page.exception_msg in e.message
            assert page.class_el.text in e.message
            assert page.query_string in e.message

    def test_exception_from_webdriver(self):
        """test that if an undefined property is referenced, valid Webdriver exception
        information is returned"""
        class SimplePage(Page):
            class_el = Element(Locators.CLASS_NAME, "simple_class")
            exception_msg = "Class Name Found"
            query_string = "key1=value1&key2=value2"
            invalid_el = Element(Locators.ID, "blargh")

        uri = make_temp_page(ElementTest.page_content)
        page = SimplePage(self.driver, uri)

        locator_failure = page.invalid_el

        try:
            text = locator_failure.text
        except Exception as e:
            assert "NoSuchElementException" in e.message
            assert "id" in e.message
            assert "blargh" in e.message

    if __name__ == "__main__":
        unittest.main()
