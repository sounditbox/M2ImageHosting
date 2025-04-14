from http.server import HTTPServer

from loguru import logger
from psycopg import connect

from ImageHostingHandler import ImageHostingHttpRequestHandler
from settings import SERVER_ADDRESS, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


def run(server_class=HTTPServer, handler_class=ImageHostingHttpRequestHandler):

    init_tables()
    httpd = server_class(SERVER_ADDRESS, handler_class)
    logger.info(f'Serving on http://{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.warning('Keyboard interrupt received, exiting.')
        httpd.server_close()
    finally:
        logger.info('Server stopped.')


def init_tables():
    with connect(f"dbname={DB_NAME} user={DB_USER} "
                 f"password={DB_PASSWORD} host={DB_HOST}") as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                original_name VARCHAR(255) NOT NULL,
                size INTEGER,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_type VARCHAR(10)
            );
            """)
            conn.commit()
            logger.info('Tables initialized.')


if __name__ == '__main__':
    run()
