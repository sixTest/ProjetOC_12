from rest_framework.exceptions import APIException
from rest_framework import status


class PermissionOnClientError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Permission on client error : You are not responsible for this client'


class UserGroupError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'User group error : the user is not part of the support group'


class PermissionOnContractError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Permission on contract error : you are not responsible for this contract'


class PermissionModificationError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Permission modification error : ' \
                     'Support group members cannot change client and event_status fields'
