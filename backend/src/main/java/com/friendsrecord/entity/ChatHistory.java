package com.friendsrecord.entity;

import lombok.Data;
import java.io.Serializable;
import java.time.LocalDateTime;

@Data
public class ChatHistory implements Serializable {
    private static final long serialVersionUID = 1L;
    private String id;
    private String sessionId;
    private String role; // user: 用户, assistant: AI
    private String content;
    private LocalDateTime createdAt;
}
