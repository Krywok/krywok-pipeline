from falcon.asgi import App, Request, Response

from pipeline.handlers.condition.registry import Condition
from pipeline.handlers.match.registry import Match
from pipeline.handlers.transform.registry import Transform
from pipeline.integration.falcon.decorator import process_request

app = App()

app.resp_options.xml_error_serialization = False


class Resource:
    @process_request(
        email={
            "type": str,
            "conditions": {
                Condition.MaxLength: 64
            },
            "matches": {
                Match.Format.Email: None
            }
        }
    )
    async def on_get_email(self, req: Request, resp: Response, email: str):
        resp.media = email

    @process_request(
        first={"type": int},
        second={
            "type": int,
            "transform": {
                Transform.Multiply: 100
            }
        }
    )
    async def on_get_number(
        self, req: Request, resp: Response, first: int, second: int
    ):
        resp.media = first + second


app.add_route("/email", Resource(), suffix="email")
app.add_route("/number", Resource(), suffix="number")
