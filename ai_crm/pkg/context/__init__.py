"""Context package."""

import typing as tp

from ai_crm.pkg.context.web_context import WebContext

AnyContext = tp.Union[WebContext]
