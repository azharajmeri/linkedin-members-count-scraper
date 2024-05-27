from core.controllers.linkedin import LinkedInController
from core.exceptions.web_driver import UnableToRenderPage

if __name__ == "__main__":
    try:
        LinkedInController().initiate()
    except UnableToRenderPage as e:
        print("Page rendering fail - {e.msg}")
    except Exception as e:
        print(f"Unknown exception occured - {e.msg}")
    print("ENDED")
