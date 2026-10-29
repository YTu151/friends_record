package com.friendsrecord.entity;

import lombok.Data;
import java.io.Serializable;
import java.time.LocalDateTime;

@Data
public class VectorRecord implements Serializable {
    private static final long serialVersionUID = 1L;
    private String id;
    private String originalId; // 原始数据ID
    private String dataType; // friend: 朋友信息, preference: 偏好, note: 便签
    private String vectorIndex; // 向量存储索引
    private String content; // 原始文本内容
    private LocalDateTime createdAt;
}
