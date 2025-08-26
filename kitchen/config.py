class BaseConfig:
    API_TITLE = 'Kitchen API' #tHE title of our API
    API_VERSION = 'v1' #The version of our API
    OPENAPI_VERSION = '3.0.3' #the version of OpenAPi we are using
    OPENAPI_JSON_PATH = 'openapi/kitchen.json'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_REDOC_PATH = '/redoc'
    OPENAPI_REDOC_URL = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'
    OPENAPI_SWAGGER_UI_PATH = '/docs/kitchen'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    OPENAPI_SWAGGER_UI_VERSION = '3.52.5'