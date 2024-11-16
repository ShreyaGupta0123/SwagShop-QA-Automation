import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class SwagShopTestSuite(unittest.TestCase):

    def setUp(self):
        # Set up the WebDriver before each test
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.saucedemo.com/")
        time.sleep(2)  # Pause to observe the page load

    def tearDown(self):
        # Pause to observe the end state before closing the browser
        time.sleep(2)
        self.driver.quit()

    def test_user_authentication(self):
        """Test Case for User Authentication"""
        driver = self.driver
        # Enter the username and password and submit the login form
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        time.sleep(1)  # Pause to observe input
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(1)  # Pause to observe input
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)  # Pause to observe the login action

        # Verify the user is redirected to the inventory page after login
        self.assertIn("inventory.html", driver.current_url, "Login failed")
        print("User authentication test passed!")

    def test_product_catalog_display(self):
        """Test Case for Verifying Product Catalog Display"""
        driver = self.driver
        # Log in to access the product catalog
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        # Check if products are displayed on the inventory page
        products = driver.find_elements(By.CLASS_NAME, "inventory_item")
        self.assertGreater(len(products), 0, "Product catalog not displayed")
        time.sleep(2)  # Pause to observe the displayed products
        print("Product catalog display test passed!")

    def test_add_all_items_to_cart(self):
        """Test Case for Adding All Products to the Cart"""
        driver = self.driver
        # Log in to access the inventory
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        # Add all items to the cart
        add_buttons = driver.find_elements(By.XPATH, "//button[text()='Add to cart']")
        for button in add_buttons:
            button.click()
            time.sleep(1)  # Pause to observe each add action

        # Verify that the cart icon shows the total number of items
        cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        self.assertEqual(cart_count, str(len(add_buttons)), "Not all items were added to the cart")
        print("All items added to cart test passed!")

    def test_remove_all_items_from_cart(self):
        """Test Case for Removing All Products from the Cart"""
        driver = self.driver
        # Log in and add all items to the cart
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        # Add all items to the cart before navigating to the cart page
        add_buttons = driver.find_elements(By.XPATH, "//button[text()='Add to cart']")
        for button in add_buttons:
            button.click()
            time.sleep(1)

        # Navigate to the cart page
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(2)

        # Remove all items from the cart
        remove_buttons = driver.find_elements(By.XPATH, "//button[text()='Remove']")
        for button in remove_buttons:
            button.click()
            time.sleep(1)  # Pause to observe each removal action

        # Verify that the cart is empty
        cart_badge = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(len(cart_badge), 0, "Not all items were removed from the cart")
        print("All items removed from cart test passed!")

    def test_product_sorting(self):
        """Test Case for Verifying Product Sorting by  Name (A to Z)"""
        driver = self.driver
        # Log in to access the inventory and sorting functionality
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

        # Sort products by price from low to high
        sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
        sort_dropdown.click()
        time.sleep(1)  # Pause to observe dropdown interaction
        driver.find_element(By.XPATH, "//option[text()='Name (A to Z)']").click()
        time.sleep(2)  # Pause to observe sorting

        # Verify that the product names are sorted correctly
        product_names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        name_values = [name.text for name in product_names]
        self.assertEqual(name_values, sorted(name_values), "Products are not sorted by name (A to Z)")
        print("Product sorting by name test passed!")

if __name__ == "__main__":
    unittest.main()