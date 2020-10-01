import uvicorn

from api import app
from mangum import Mangum

lambda_handler = Mangum(app)

if __name__ == '__main__':
    uvicorn.run(app, )
