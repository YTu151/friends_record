package com.friendsrecord.entity;

import lombok.Data;
import java.io.Serializable;
import java.time.LocalDateTime;

@Data
public class Note implements Serializable {
    private static final long serialVersionUID = 1L;
    private String id;
    private String friendId;
    private String title;
    private String content;
    private LocalDateTime noteTime;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    // 关联数据
    private String friendName;
}
