class TabHandler:
    def __init__(self, driver_manager, element_locator, ws, wb, excel_file):
        self.driver_manager = driver_manager
        self.element_locator = element_locator
        self.ws = ws
        self.wb = wb
        self.excel_file = excel_file

    def open_urls_in_tabs(self, urls):
        # Open the first tab
        self.driver_manager.navigate_to(urls[0])
        # Open the other 9 tabs
        for i in range(1, min(10, len(urls))):
            print(f"Assigning new URL: {urls[i]}")
            self.driver_manager.open_new_tab(urls[i])

        # Process remaining URLs
        remaining_urls = urls[10:]
        count = len(urls)
        completed_urls = []
        while count > 1:
            for handle in self.driver_manager.driver.window_handles:
                self.driver_manager.driver.switch_to.window(handle)
                if self.check_page_loaded() and self.driver_manager.driver.current_url not in completed_urls:
                    count -= 1
                    print(count)
                    if element := self.driver_manager.find_element(self.element_locator):
                        self.ws.append(
                            [self.driver_manager.driver.current_url,
                             element.get_attribute("textContent").replace("associated members", "").strip()])
                    else:
                        self.ws.append(f"Unable to extract data for: {self.driver_manager.driver.current_url}")
                    completed_urls.append(self.driver_manager.driver.current_url)

                    self.wb.save(self.excel_file)
                    # Assign a new URL from the remaining list
                    if remaining_urls:
                        new_url = remaining_urls.pop(0)
                        print(f"Assigning new URL: {new_url}")
                        self.driver_manager.navigate_to(new_url)

    def check_page_loaded(self):
        try:
            self.driver_manager.driver.execute_script("return document.readyState") == "complete"
            return True
        except Exception:
            return False
