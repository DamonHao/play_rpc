# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rpc.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='rpc.proto',
  package='play_rpc.net.rpc',
  syntax='proto3',
  serialized_pb=_b('\n\trpc.proto\x12\x10play_rpc.net.rpc\"\xb5\x01\n\nRpcMessage\x12+\n\x04type\x18\x01 \x01(\x0e\x32\x1d.play_rpc.net.rpc.MessageType\x12\n\n\x02id\x18\x02 \x01(\x06\x12\x0f\n\x07service\x18\x03 \x01(\t\x12\x0e\n\x06method\x18\x04 \x01(\t\x12\x0f\n\x07request\x18\x05 \x01(\x0c\x12\x10\n\x08response\x18\x06 \x01(\x0c\x12*\n\x05\x65rror\x18\x07 \x01(\x0e\x32\x1b.play_rpc.net.rpc.ErrorCode*3\n\x0bMessageType\x12\x0b\n\x07REQUEST\x10\x00\x12\x0c\n\x08RESPONSE\x10\x01\x12\t\n\x05\x45RROR\x10\x02*\x81\x01\n\tErrorCode\x12\x0c\n\x08NO_ERROR\x10\x00\x12\x0f\n\x0bWRONG_PROTO\x10\x01\x12\x0e\n\nNO_SERVICE\x10\x02\x12\r\n\tNO_METHOD\x10\x03\x12\x13\n\x0fINVALID_REQUEST\x10\x04\x12\x14\n\x10INVALID_RESPONSE\x10\x05\x12\x0b\n\x07TIMEOUT\x10\x06\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_MESSAGETYPE = _descriptor.EnumDescriptor(
  name='MessageType',
  full_name='play_rpc.net.rpc.MessageType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='REQUEST', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RESPONSE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=215,
  serialized_end=266,
)
_sym_db.RegisterEnumDescriptor(_MESSAGETYPE)

MessageType = enum_type_wrapper.EnumTypeWrapper(_MESSAGETYPE)
_ERRORCODE = _descriptor.EnumDescriptor(
  name='ErrorCode',
  full_name='play_rpc.net.rpc.ErrorCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NO_ERROR', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WRONG_PROTO', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NO_SERVICE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NO_METHOD', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_REQUEST', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_RESPONSE', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TIMEOUT', index=6, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=269,
  serialized_end=398,
)
_sym_db.RegisterEnumDescriptor(_ERRORCODE)

ErrorCode = enum_type_wrapper.EnumTypeWrapper(_ERRORCODE)
REQUEST = 0
RESPONSE = 1
ERROR = 2
NO_ERROR = 0
WRONG_PROTO = 1
NO_SERVICE = 2
NO_METHOD = 3
INVALID_REQUEST = 4
INVALID_RESPONSE = 5
TIMEOUT = 6



_RPCMESSAGE = _descriptor.Descriptor(
  name='RpcMessage',
  full_name='play_rpc.net.rpc.RpcMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='play_rpc.net.rpc.RpcMessage.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='id', full_name='play_rpc.net.rpc.RpcMessage.id', index=1,
      number=2, type=6, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='service', full_name='play_rpc.net.rpc.RpcMessage.service', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='method', full_name='play_rpc.net.rpc.RpcMessage.method', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='request', full_name='play_rpc.net.rpc.RpcMessage.request', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='response', full_name='play_rpc.net.rpc.RpcMessage.response', index=5,
      number=6, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error', full_name='play_rpc.net.rpc.RpcMessage.error', index=6,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=213,
)

_RPCMESSAGE.fields_by_name['type'].enum_type = _MESSAGETYPE
_RPCMESSAGE.fields_by_name['error'].enum_type = _ERRORCODE
DESCRIPTOR.message_types_by_name['RpcMessage'] = _RPCMESSAGE
DESCRIPTOR.enum_types_by_name['MessageType'] = _MESSAGETYPE
DESCRIPTOR.enum_types_by_name['ErrorCode'] = _ERRORCODE

RpcMessage = _reflection.GeneratedProtocolMessageType('RpcMessage', (_message.Message,), dict(
  DESCRIPTOR = _RPCMESSAGE,
  __module__ = 'rpc_pb2'
  # @@protoc_insertion_point(class_scope:play_rpc.net.rpc.RpcMessage)
  ))
_sym_db.RegisterMessage(RpcMessage)


# @@protoc_insertion_point(module_scope)
