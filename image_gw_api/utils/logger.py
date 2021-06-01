from datetime import datetime, timezone

from aiologger import Logger
from aiologger.formatters.json import (
    JsonFormatter,
    LOG_LEVEL_FIELDNAME,
    LOGGED_AT_FIELDNAME,
    LINE_NUMBER_FIELDNAME,
    FUNCTION_NAME_FIELDNAME,
    MSG_FIELDNAME,
)
from aiologger.levels import LEVEL_TO_NAME, LogLevel
from aiologger.records import LogRecord

from image_gw_api.constants import SERVICE_NAME, LOG_SERVICE_NAME


class CustomFormatter(JsonFormatter):
    level_to_name_mapping = LEVEL_TO_NAME

    def formatter_fields_for_record(self, record: LogRecord):
        """
        :type record: aiologger.records.ExtendedLogRecord
        """
        datetime_serialized = (
            datetime.now(timezone.utc).astimezone().isoformat()
        )

        default_fields = (
            (LOG_SERVICE_NAME, record.name),
            (LOGGED_AT_FIELDNAME, datetime_serialized),
            (LINE_NUMBER_FIELDNAME, record.lineno),
            (FUNCTION_NAME_FIELDNAME, record.funcName),
            (LOG_LEVEL_FIELDNAME, self.level_to_name_mapping[record.levelno]),
            (MSG_FIELDNAME, record.msg),
        )

        for field, value in default_fields:
            yield field, value

    def format(self, record: LogRecord) -> str:
        """
        Formats a record and serializes it as a JSON str. If record message isnt
        already a dict, initializes a new dict and uses `default_msg_fieldname`
        as a key as the record msg as the value.
        """
        msg = dict(self.formatter_fields_for_record(record))

        if record.exc_info:
            msg["exc_info"] = record.exc_info
        if record.exc_text:
            msg["exc_text"] = record.exc_text

        return self.serializer(msg, default=self._default_handler)


log = Logger.with_default_handlers(name=SERVICE_NAME, level=LogLevel.DEBUG, formatter=CustomFormatter())
