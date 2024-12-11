import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

class SwagShopTestSuite(unittest.TestCase):

    def setUp(self):
        # Set up the WebDriver before each test
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        time.sleep(2)  # Pause to observe the page load

    def tearDown(self):
        """Quit WebDriver after each test."""
        time.sleep(2)
        self.driver.quit()

    def login(self, username="standard_user", password="secret_sauce"):
        """Reusable login method."""
        driver = self.driver
        driver.find_element(By.ID, "user-name").send_keys(username)
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys(password)
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)

    def test_user_authentication(self):
        """TC01: Test Case for User Authentication."""
        print("Starting TC01: Testing user authentication functionality.")
        # Login to the application
        print("Logging into the application with valid credentials...")
        self.login()
        print("Login action performed. Verifying redirection to the inventory page...")
        # The user should be redirected to the inventory page
        self.assertIn("inventory.html", self.driver.current_url, "Login failed.")
        print("Redirection to the inventory page verified successfully.")
        # Log a success message if the test passes
        print("TC01: User authentication test passed!")

    def test_product_catalog_display(self):
        """TC02: Test Case for Verifying Product Catalog Display."""
        print("Starting TC02: Testing product catalog display functionality.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Check if products are displayed on the inventory page
        print("Verifying if the product catalog is displayed on the inventory page...")
        products = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
        self.assertGreater(len(products), 0, "Product catalog not displayed.")
        print(f"Product catalog contains {len(products)} items. Verified successfully.")
        # Log test success
        print("TC02: Product catalog display test passed!")

    def test_add_all_products_to_cart(self):
        """TC03: Test Case for Adding All Products to the Cart."""
        print("Starting TC03: Testing add all products to cart functionality.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Locate all "Add to cart" buttons and click each
        print("Adding all products to the cart...")
        add_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Add to cart']")
        for index, button in enumerate(add_buttons):
            button.click()
            print(f"Added product {index + 1} to the cart.")
            time.sleep(1)
        # Verify that all "Add to Cart" buttons change to "Remove"
        print("Verifying that all 'Add to Cart' buttons have changed to 'Remove'...")
        remove_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Remove']")
        self.assertEqual(
            len(remove_buttons),
            len(add_buttons),
            "Not all products were successfully marked as added to the cart."
        )
        print(f"All {len(remove_buttons)} products are marked as added to the cart. Verified successfully.")
        # Log test success
        print("TC03: All products added to cart test passed!")

    def test_remove_all_product_from_cart(self):
        """TC04: Test Case for Removing All Products from the Cart."""
        print("Starting TC04: Testing remove all products from cart functionality.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Locate all "Add to cart" buttons and click each
        print("Adding all products to the cart before removal...")
        add_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Add to cart']")
        for index, button in enumerate(add_buttons):
            button.click()
            print(f"Added product {index + 1} to the cart.")
            time.sleep(1)
        # Navigate to the cart page
        print("Navigating to the cart page...")
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        print("Navigated to the cart page successfully.")
        time.sleep(2)
        # Remove all products from the cart
        print("Removing all products from the cart...")
        remove_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Remove']")
        for index, button in enumerate(remove_buttons):
            button.click()
            print(f"Removed product {index + 1} from the cart.")
            time.sleep(1)
        # Verify that the cart is empty
        print("Verifying that the cart is empty...")
        cart_badge = self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(len(cart_badge), 0, "Not all items were removed from the cart.")
        print("Cart is empty. Verified successfully.")
        # Log test success
        print("TC04: All products removed from cart test passed!")

    def test_product_sorting(self):
        """TC05: Test Case for Verifying Product Sorting by Name (A to Z)."""
        print("Starting TC05: Testing product sorting functionality.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Open the sort dropdown and select "Name (A to Z)"
        print("Opening the sort dropdown menu...")
        sort_dropdown = self.driver.find_element(By.CLASS_NAME, "product_sort_container")
        sort_dropdown.click()
        print("Dropdown menu opened. Selecting 'Name (A to Z)' option...")
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//option[text()='Name (A to Z)']").click()
        time.sleep(2)
        print("Selected 'Name (A to Z)' sorting option.")
        # Verify the product names are sorted correctly
        print("Verifying that the product names are sorted correctly...")
        product_names = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        name_values = [name.text for name in product_names]
        self.assertEqual(name_values, sorted(name_values), "Products are not sorted by name.")
        print("Verified that the product names are sorted in ascending order (A to Z).")
        # Log test success
        print("TC05: Product sorting by name test passed!")

    def test_view_products_in_cart(self):
        """TC06: Test Case for Viewing Products in the Cart."""
        print("Starting TC06: Testing view products in cart functionality.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Add a single product to the cart
        print("Adding a product to the cart...")
        self.driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
        time.sleep(1)
        print("Product added to the cart successfully.")
        # Click the cart icon to view cart contents
        print("Navigating to the cart page...")
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        print("Navigated to the cart page successfully.")
        # Verify the cart contains the added product
        print("Verifying that the cart contains the added product...")
        cart_items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        self.assertEqual(len(cart_items), 1, "Cart items not displayed correctly.")
        print("Verified that the cart contains the added product.")
        # Log test success
        print("TC06: View products in cart test passed!")

    def test_logout(self):
        """TC07: Test Case for Verifying Logout Functionality."""
        print("Starting TC07: Testing logout functionality.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Open the sidebar menu
        print("Opening the sidebar menu...")
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()
        time.sleep(1)
        print("Sidebar menu opened successfully.")
        # Hover over the 'All Items' link
        action = ActionChains(self.driver)
        logout_link = self.driver.find_element(By.ID, "logout_sidebar_link")
        logout_link.value_of_css_property("color")
        action.move_to_element(logout_link).perform()
        time.sleep(1)
        logout_link.value_of_css_property("color")
        # Click the logout link
        print("Clicking the logout link...")
        self.driver.find_element(By.ID, "logout_sidebar_link").click()
        print("Logout link clicked. Verifying redirection to the login page...")
        # Verify redirection to the login page
        self.assertIn("https://www.saucedemo.com/", self.driver.current_url, "Logout failed.")
        print("Verified redirection to the login page.")
        # Log test success
        print("TC07: Logout test passed!")

    def test_cart_quantity_display(self):
        """TC08: Test Case for Verifying Cart Quantity Display."""
        print("Starting TC08: Testing cart quantity display functionality.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Add a single product to the cart
        print("Adding a single product to the cart...")
        self.driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
        print("Product added to the cart successfully.")
        # Verify the cart badge displays the correct item count
        print("Verifying the cart badge displays the correct item count...")
        cart_badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
        self.assertEqual(cart_badge, "1", "Cart quantity is incorrect.")
        print("Verified that the cart badge displays the correct item count.")
        # Log test success
        print("TC08: Cart quantity display test passed!")

    def test_first_name_error_validation(self):
        """TC09: Validate error message for missing 'First Name' field during checkout."""
        driver = self.driver
        print("Starting TC09: Testing First Name error validation.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Add a product to the cart
        print("Adding a product to the cart...")
        driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
        time.sleep(2)
        print("Product added to the cart successfully.")
        # Navigate to the cart page
        print("Navigating to the cart page...")
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(2)
        print("Navigated to the cart page successfully.")
        # Proceed to the checkout page
        print("Proceeding to the checkout page...")
        driver.find_element(By.ID, "checkout").click()
        time.sleep(2)
        print("Proceeded to the checkout page successfully.")
        # Leave the 'First Name' field blank and fill in other fields
        print("Filling in Last Name and Postal Code while leaving First Name blank...")
        driver.find_element(By.ID, "last-name").send_keys("Addams")
        time.sleep(2)
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        time.sleep(2)
        print("Required fields filled in except First Name.")
        # Click the 'Continue' button
        print("Clicking the 'Continue' button...")
        driver.find_element(By.ID, "continue").click()
        # Verify the error message for the missing 'First Name' field
        print("Verifying the error message for missing 'First Name' field...")
        error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
        self.assertEqual(error_message, "Error: First Name is required",
                         "Error message for missing 'First Name' is incorrect.")
        print("Verified the error message successfully.")
        # Log test success
        print("TC09: First Name validation test passed!")

    def test_total_amount_display(self):
        """TC10: Test Case for Verifying Overall Total Display in Checkout."""
        driver = self.driver
        print("Starting TC10: Testing Total Amount display in checkout.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Add products to the cart
        print("Adding products to the cart...")
        driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
        driver.find_element(By.XPATH, "(//button[text()='Add to cart'])[2]").click()
        time.sleep(2)
        print("Products added to the cart successfully.")
        # Navigate to the cart page
        print("Navigating to the cart page...")
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(2)
        print("Navigated to the cart page successfully.")
        # Proceed to the checkout information page
        print("Proceeding to the checkout information page...")
        driver.find_element(By.ID, "checkout").click()
        time.sleep(2)
        print("Proceeded to the checkout information page successfully.")
        # Fill in the required information and continue
        print("Filling in the required checkout information...")
        driver.find_element(By.ID, "first-name").send_keys("Wednesday")
        time.sleep(2)
        driver.find_element(By.ID, "last-name").send_keys("Addams")
        time.sleep(2)
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        time.sleep(2)
        print("Required checkout information filled in successfully.")
        print("Clicking the 'Continue' button...")
        driver.find_element(By.ID, "continue").click()
        time.sleep(3)
        print("Proceeded to the checkout overview page successfully.")
        # Verify the overall total on the checkout overview page
        print("Verifying the overall total on the checkout overview page...")
        item_total = driver.find_element(By.CLASS_NAME, "summary_subtotal_label").text.split("$")[1]
        tax_total = driver.find_element(By.CLASS_NAME, "summary_tax_label").text.split("$")[1]
        overall_total = driver.find_element(By.CLASS_NAME, "summary_total_label").text.split("$")[1]
        print(f"Item Total: {item_total}, Tax: {tax_total}, Displayed Overall Total: {overall_total}")
        # Convert totals to float for calculation
        calculated_total = round(float(item_total) + float(tax_total), 2)
        displayed_total = round(float(overall_total), 2)
        print(f"Calculated Total: {calculated_total}, Displayed Total: {displayed_total}")
        # Assert that the displayed total matches the calculated total
        self.assertEqual(calculated_total, displayed_total,
                         "Overall total does not match the sum of item total and tax.")
        print("Verified the total amount successfully.")
        # Log test success
        print("TC10: Total amount display test passed!")

    def test_all_items_link(self):
        """TC11: Test 'All Items' link redirects to the inventory page."""
        driver = self.driver
        print("Starting TC11: Testing 'All Items' link functionality.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Navigate to the cart page
        print("Navigating to the cart page...")
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(2)
        print("Navigated to the cart page successfully.")
        # Open the sidebar menu
        print("Opening the sidebar menu...")
        driver.find_element(By.ID, "react-burger-menu-btn").click()
        time.sleep(1)
        print("Sidebar menu opened successfully.")
        # Hover over the 'All Items' link
        action = ActionChains(driver)
        all_items_link = driver.find_element(By.ID, "inventory_sidebar_link")
        all_items_link.value_of_css_property("color")
        action.move_to_element(all_items_link).perform()
        time.sleep(1)
        all_items_link.value_of_css_property("color")
        # Click the All Items link
        print("Clicking the 'All Items' link...")
        driver.find_element(By.ID, "inventory_sidebar_link").click()
        time.sleep(2)
        print("Clicked the 'All Items' link successfully.")
        # Verify redirection to the inventory page
        print("Verifying redirection to the inventory page...")
        self.assertIn("inventory.html", driver.current_url, "All Items link did not redirect to the inventory page")
        print("Verified redirection to the inventory page successfully.")
        # Log test success
        print("TC11: All Items link test passed!")

    def test_reset_app_state(self):
        """TC12: Test 'Reset App State' functionality."""
        driver = self.driver
        print("Starting TC12: Testing 'Reset App State' functionality.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Add a product to the cart
        print("Adding a product to the cart...")
        self.driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
        time.sleep(3)
        print("Product added to the cart successfully.")
        # Open the sidebar menu
        print("Opening the sidebar menu...")
        self.driver.find_element(By.ID, "react-burger-menu-btn").click()
        time.sleep(1)
        print("Sidebar menu opened successfully.")
        # Hover over the 'Reset App State' link
        action = ActionChains(driver)
        reset_app_link = driver.find_element(By.ID, "reset_sidebar_link")
        reset_app_link.value_of_css_property("color")
        action.move_to_element(reset_app_link).perform()
        time.sleep(1)
        reset_app_link.value_of_css_property("color")
        # Click the Reset App State link
        print("Clicking the 'Reset App State' link...")
        self.driver.find_element(By.ID, "reset_sidebar_link").click()
        time.sleep(2)
        print("'Reset App State' link clicked successfully.")
        # Verify that the cart is empty
        print("Verifying the cart badge icon...")
        cart_badge = self.driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(len(cart_badge), 0, "Cart was not cleared by 'Reset App State'.")
        print("Verified that the cart icon badge disappeared.")
        # Log test success
        print("TC12: 'Reset App State' test passed!")

    def test_image_click_ability(self):
        """TC13: Test product image redirects to product detail page."""
        print("Starting TC13: Testing product image click functionality.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Find the first product image on the inventory page
        print("Locating the first product image on the inventory page...")
        product_image = self.driver.find_element(By.CLASS_NAME, "inventory_item_img")
        # Click the product image
        print("Clicking the product image...")
        product_image.click()
        time.sleep(2)
        print("Clicked the product image successfully.")
        # Verify navigation to the product detail page
        print("Verifying navigation to the product detail page...")
        self.assertIn("inventory-item", self.driver.current_url, "Product image did not navigate to the detail page.")
        print("Verified navigation to the product detail page.")
        # Log a success message if the test passes
        print("TC13: Product image click ability test passed!")

    def test_back_home_navigation(self):
        """TC14: Verify the functionality of the Back Home button on the order confirmation page."""
        driver = self.driver
        print("Starting TC21: Back Home Navigation Test.")
        # Log into the application
        print("Logging into the application...")
        self.login()
        print("Logged in successfully.")
        # Add the first product to the cart
        print("Adding a product to the cart...")
        driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
        time.sleep(2)
        print("Product added to the cart successfully.")
        # Navigate to the cart and proceed to checkout
        print("Navigating to the cart page...")
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(2)
        print("Proceeding to the checkout page...")
        driver.find_element(By.ID, "checkout").click()
        time.sleep(2)
        # Fill in checkout details and finish the order
        print("Filling in checkout details...")
        driver.find_element(By.ID, "first-name").send_keys("Wednesday")
        time.sleep(1)
        driver.find_element(By.ID, "last-name").send_keys("Addams")
        time.sleep(1)
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        time.sleep(1)
        print("Continuing to the checkout overview page...")
        driver.find_element(By.ID, "continue").click()
        time.sleep(2)
        print("Completing the order...")
        driver.find_element(By.ID, "finish").click()
        time.sleep(2)
        # Verify redirection to the order confirmation page
        print("Verifying redirection to the order confirmation page...")
        self.assertIn("checkout-complete.html", driver.current_url, "Failed to reach the order confirmation page.")
        print("Order confirmation page verified successfully.")
        # Click the "Back Home" button
        print("Clicking the 'Back Home' button...")
        driver.find_element(By.ID, "back-to-products").click()
        time.sleep(2)
        # Verify redirection to the inventory page
        print("Verifying redirection to the inventory page...")
        self.assertIn("inventory.html", driver.current_url,
                      "'Back Home' button did not navigate to the inventory page.")
        print("Verified redirection to the inventory page successfully.")
        print("TC21: Back Home Navigation Test passed successfully!")

    def test_back_to_products_link(self):
        """TC15: Test 'Back to Products' link navigates back to the inventory page."""
        driver = self.driver
        print("Starting TC15: Testing 'Back to Products' link functionality.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Locate and click on the first product image
        print("Clicking on a product image to navigate to the product detail page...")
        product_image = driver.find_element(By.CLASS_NAME, "inventory_item_img")
        product_image.click()
        time.sleep(2)
        # Verify that the product detail page is displayed
        print("Verifying navigation to the product detail page...")
        self.assertIn("inventory-item", driver.current_url, "Failed to navigate to the product detail page.")
        print("Navigation to product detail page verified successfully.")
        # Locate and click the 'Back to Products' link
        print("Locating and clicking the 'Back to Products' button...")
        back_to_products_button = driver.find_element(By.ID, "back-to-products")
        print("'Back to Products' button located successfully.")
        # Hover over the 'Back to Products' button
        action = ActionChains(driver)
        action.move_to_element(back_to_products_button).perform()
        time.sleep(1)
        # Click the button to navigate back to the inventory page
        back_to_products_button.click()
        time.sleep(2)
        print("Clicked 'Back to Products' button successfully.")
        # Verify that the user is navigated back to the inventory page
        print("Verifying navigation back to the inventory page...")
        self.assertIn("inventory.html", driver.current_url, "Failed to navigate back to the inventory page.")
        print("Verified navigation back to the inventory page successfully.")
        # Log test success
        print("TC15: 'Back to Products' link test passed!")

    def test_finish_button_functionality(self):
        """TC16: Test the 'Finish' button completes the checkout."""
        driver = self.driver
        print("Starting TC16: Testing 'Finish' button functionality during checkout.")
        # Login to the application
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Add the first product to the cart by locating and clicking the "Add to cart" button
        print("Adding the first product to the cart...")
        driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
        time.sleep(2)
        print("Product added to the cart successfully.")
        # Navigate to the cart page by clicking the shopping cart link
        print("Navigating to the cart page...")
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(2)
        print("Navigated to the cart page successfully.")
        # Proceed to the checkout page by clicking the "Checkout" button
        print("Proceeding to the checkout page...")
        driver.find_element(By.ID, "checkout").click()
        time.sleep(2)
        print("Proceeded to the checkout page successfully.")
        # Enter the required checkout information (First Name, Last Name, and Postal Code)
        print("Entering required checkout information...")
        driver.find_element(By.ID, "first-name").send_keys("Wednesday")
        time.sleep(2)
        driver.find_element(By.ID, "last-name").send_keys("Addams")
        time.sleep(2)
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        time.sleep(2)
        print("Entered required checkout information successfully.")
        # Continue to the checkout overview page by clicking the "Continue" button
        print("Proceeding to the checkout overview page...")
        driver.find_element(By.ID, "continue").click()
        time.sleep(2)
        print("Proceeded to the checkout overview page successfully.")
        # Complete the checkout process by clicking the "Finish" button
        print("Completing the checkout process by clicking the 'Finish' button...")
        driver.find_element(By.ID, "finish").click()
        time.sleep(2)
        print("Clicked 'Finish' button successfully.")
        # Verify that the user is redirected to the order confirmation page
        print("Verifying redirection to the order confirmation page...")
        self.assertIn("checkout-complete.html", driver.current_url,
                      "Finish button did not complete the checkout process.")
        print("Redirection to the order confirmation page verified successfully.")
        # Log a success message if the test passes
        print("TC16: Finish button functionality test passed!")

    def test_menu_bar_functionality(self):
        """TC17: Test the menu icon opens and closes the sidebar."""
        driver = self.driver
        # Login to the application
        print("Starting test: Menu Bar Functionality")
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(1)
        # Locate the menu icon and click to open the sidebar
        print("Locating the menu icon...")
        menu_button = driver.find_element(By.ID, "react-burger-menu-btn")
        print("Menu icon located. Clicking to open the sidebar...")
        menu_button.click()
        time.sleep(2)
        # Verify that the menu sidebar is displayed after clicking the menu icon
        print("Verifying that the menu sidebar is displayed...")
        menu_sidebar = driver.find_element(By.CLASS_NAME, "bm-menu-wrap")
        self.assertTrue(menu_sidebar.is_displayed(), "Menu sidebar did not open")
        print("Menu sidebar is displayed successfully.")
        # Locate the close button (X icon) on the sidebar and click it to close the sidebar
        print("Locating the close button (X icon) on the sidebar...")
        driver.find_element(By.ID, "react-burger-cross-btn").click()
        print("Close button located. Clicking to close the sidebar...")
        time.sleep(2)
        # Verify that the menu sidebar is no longer displayed after closing it
        print("Verifying that the menu sidebar is no longer displayed...")
        self.assertFalse(menu_sidebar.is_displayed(), "Menu sidebar did not close")
        print("Menu sidebar closed successfully.")
        # Log a success message if the test passes
        print("TC17: Menu bar functionality test passed!")

    def test_continue_shopping(self):
        """TC18: Test 'Continue Shopping' button on cart page."""
        driver = self.driver
        # Start the test case
        print("Starting test: Continue Shopping Button on Cart Page.")
        # Login to the application
        self.login()
        time.sleep(2)
        print("Logged in to the application successfully. Navigated to the inventory page.")
        # Add a product to the cart
        print("Adding a product to the cart...")
        driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
        time.sleep(2)
        print("Product successfully added to the cart.")
        # Navigate to the cart page
        print("Navigating to the cart page...")
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(2)
        print("Successfully navigated to the cart page.")
        # Click the 'Continue Shopping' button
        print("Clicking the 'Continue Shopping' button...")
        driver.find_element(By.ID, "continue-shopping").click()
        time.sleep(2)
        print("Clicked the 'Continue Shopping' button successfully.")
        # Verify navigation back to the inventory page
        print("Verifying navigation back to the inventory page...")
        self.assertIn("inventory.html", driver.current_url,
                      "'Continue Shopping' button did not navigate to the inventory page")
        print("Verified navigation back to the inventory page successfully.")
        # Log a success message if the test passes
        print("TC18: 'Continue Shopping' button test passed!")

    def test_cancel_button_on_checkout(self):
        """TC19: Test 'Cancel' button functionality on the checkout page."""
        driver = self.driver
        # Login to the application
        print("Starting test: Cancel Button on Checkout")
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Locate and click the 'Add to cart' button for one of the products
        print("Adding a product to the cart...")
        driver.find_element(By.XPATH, "//button[text()='Add to cart']").click()
        print("Product added to the cart successfully.")
        time.sleep(2)
        # Locate and click the cart icon in the top-right corner of the page
        print("Navigating to the cart page...")
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        print("Navigated to the cart page successfully.")
        time.sleep(2)
        # Locate and click the 'Checkout' button to proceed to the checkout page
        print("Proceeding to the checkout page...")
        driver.find_element(By.ID, "checkout").click()
        print("Proceeded to the checkout page successfully.")
        time.sleep(2)
        # Locate and click the 'Cancel' button to return to the cart page
        print("Clicking the 'Cancel' button on the checkout page...")
        driver.find_element(By.ID, "cancel").click()
        print("Clicked the 'Cancel' button successfully.")
        time.sleep(2)
        # Verify navigation back to the cart page
        print("Verifying navigation back to the cart page...")
        self.assertIn("cart.html", driver.current_url,
                      "'Cancel' button did not navigate back to the cart page")
        print("Verified that the 'Cancel' button navigated back to the cart page successfully.")
        # Log a success message if the test passes
        print("TC19: 'Cancel' button on checkout test passed!")

    def test_facebook_link(self):
        """TC20: Test Facebook link functionality."""
        driver = self.driver
        # Login to the application
        print("Starting test: Facebook Link Functionality")
        self.login()
        print("Logged in to the application successfully.")
        time.sleep(2)
        # Scroll down to the footer section
        print("Scrolling down to the footer section...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("Scrolled to the footer section successfully.")
        # Locate the Facebook link in the footer section
        print("Locating the Facebook link in the footer section...")
        facebook_link = driver.find_element(By.CLASS_NAME, "social_facebook")
        print("Facebook link located successfully.")
        time.sleep(2)
        # Click the Facebook link
        print("Clicking the Facebook link to open the Facebook page in a new tab...")
        facebook_link.click()
        time.sleep(5)
        # Switch to the newly opened browser tab
        print("Switching to the new browser tab...")
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)
        print("Switched to the new browser tab successfully.")
        # Verify the URL of the new tab
        print("Verifying that the Facebook link navigates to the correct page...")
        self.assertIn("facebook.com", driver.current_url, "Facebook link did not navigate to the correct page")
        print("Verified that the Facebook link navigated to the correct page successfully.")
        # Log a success message if the test passes
        print("TC20: Facebook link test passed!")

if __name__ == "__main__":
    unittest.main()