/// ~english
/// The stream message chunk status.
/// ~end
///
/// ~chinese
/// 流式消息块状态。
/// ~end
enum StreamStatus {
  /// ~english
  /// Stream started.
  /// ~end
  ///
  /// ~chinese
  /// 流式消息开始。
  /// ~end
  START,

  /// ~english
  /// Stream started and completed in one chunk (single fragment).
  /// ~end
  ///
  /// ~chinese
  /// 流式消息开始即完成（单片流式消息）。
  /// ~end
  START_AND_COMPLETE,

  /// ~english
  /// Stream in progress.
  /// ~end
  ///
  /// ~chinese
  /// 流式消息进行中。
  /// ~end
  PROGRESS,

  /// ~english
  /// Stream completed.
  /// ~end
  ///
  /// ~chinese
  /// 流式消息完成。
  /// ~end
  COMPLETE,

  /// ~english
  /// Stream ended with error.
  /// ~end
  ///
  /// ~chinese
  /// 流式消息错误。
  /// ~end
  ERROR,
}

/// ~english
/// The stream message chunk.
/// ~end
///
/// ~chinese
/// 流式消息块。
/// ~end
class StreamChunk {
  /// ~english
  /// The stream status.
  /// ~end
  ///
  /// ~chinese
  /// 流式消息状态。
  /// ~end
  final StreamStatus status;

  /// ~english
  /// The error code.
  /// ~end
  ///
  /// ~chinese
  /// 错误码。
  /// ~end
  final int errorCode;

  /// ~english
  /// The finish reason.
  /// ~end
  ///
  /// ~chinese
  /// 完成原因。
  /// ~end
  final int finishReason;

  /// ~english
  /// The text content of the stream chunk.
  /// ~end
  ///
  /// ~chinese
  /// 流式消息块的文本内容。
  /// ~end
  final String chunk;

  /// ~english
  /// The custom type.
  /// ~end
  ///
  /// ~chinese
  /// 自定义类型。
  /// ~end
  final String? customType;

  StreamChunk._private({
    required this.status,
    required this.errorCode,
    required this.finishReason,
    required this.chunk,
    this.customType,
  });

  /// ~english
  /// Creates a stream chunk from a JSON map.
  ///
  /// Param [map] The JSON map.
  ///
  /// **Return** The stream chunk instance.
  /// ~end
  ///
  /// ~chinese
  /// 从 JSON map 创建流式消息块。
  ///
  /// Param [map] JSON map。
  ///
  /// **Return** 流式消息块实例。
  /// ~end
  factory StreamChunk.fromJson(Map<String, dynamic> map) {
    return StreamChunk._private(
      status: _streamStatusFromInt(map['status'] ?? 3),
      errorCode: map['errorCode'] ?? 0,
      finishReason: map['finishReason'] ?? 0,
      chunk: map['text'] ?? '',
      customType: map['customType'] ?? '',
    );
  }

  static StreamStatus _streamStatusFromInt(int status) {
    switch (status) {
      case 0:
        return StreamStatus.START;
      case 1:
        return StreamStatus.START_AND_COMPLETE;
      case 2:
        return StreamStatus.PROGRESS;
      case 3:
        return StreamStatus.COMPLETE;
      case 4:
        return StreamStatus.ERROR;
      default:
        return StreamStatus.COMPLETE;
    }
  }
}
