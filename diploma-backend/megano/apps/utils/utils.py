from rest_framework.response import Response


class BaseView:

    def _build_response(self, status, logger, data=None, serializer=None, many=False):
        """
        Построение ответа.

        Attributes:
            data: Данные ответа.
        """
        logger.info('Construction of the answer.')
        if data is None:
            return Response(status=status)
        serializer = serializer(data, many=many)
        return Response(serializer.data, status=status)

    def _handle_error(self, message, status, logger):
        """
        Построение ответа ошибки.

        Attributes:
            message: Сообщение ошибки.
            status: Статус код ошибки.
        """
        logger.error(message)
        return Response({'error': message}, status=status)