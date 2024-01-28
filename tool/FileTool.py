from pymysql.converters import escape_str
from flask_restful import current_app
import traceback


class FileTool:

    @staticmethod
    def get_file_content(path: str) -> str:
        try:
            current_app.logger.info('path:{}'.format(path))
            file = open(path, 'rU', encoding='utf-8')
            content = file.read()
            return content
        except Exception as err:
            current_app.logger.error(traceback.format_exc())
            raise err
        finally:
            file.close()
