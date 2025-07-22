class PresentationException(Exception):
    def __init__(self, message: str, code: str = "PRESENTATION_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)

class ContentGenerationException(PresentationException):
    def __init__(self, message: str = "Content generation failed"):
        super().__init__(message, "CONTENT_GENERATION_ERROR")

class PPTXGenerationException(PresentationException):
    def __init__(self, message: str = "PPTX generation failed"):
        super().__init__(message, "PPTX_GENERATION_ERROR")