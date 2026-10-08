from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from jobastra_ai.documents import PDFTextExtractionError
from jobastra_ai.llm.errors import (
    LLMConfigurationError,
    LLMInvocationError,
    LLMOutputValidationError,
    LLMTimeoutError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(PDFTextExtractionError)
    async def handle_pdf_error(
        _request: Request,
        exc: PDFTextExtractionError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(LLMTimeoutError)
    async def handle_llm_timeout(
        _request: Request,
        exc: LLMTimeoutError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(LLMOutputValidationError)
    async def handle_llm_output_error(
        _request: Request,
        exc: LLMOutputValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"detail": str(exc)},
        )

    @app.exception_handler(LLMInvocationError)
    async def handle_llm_invocation_error(
        _request: Request,
        exc: LLMInvocationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"detail": str(exc)},
        )

    @app.exception_handler(LLMConfigurationError)
    async def handle_llm_configuration_error(
        _request: Request,
        _exc: LLMConfigurationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "The language model is not configured correctly"},
        )
