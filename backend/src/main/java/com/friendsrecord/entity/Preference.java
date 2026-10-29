package com.friendsrecord.entity;

import lombok.Data;
import java.io.Serializable;
import java.time.LocalDateTime;

@Data
public class Preference implements Serializable {
    private static final long serialVersionUID = 1L;
    private String id;
    private String friendId;
    private String type; // like: 喜好, dislike: 厌恶
    private String content;
    private String tag;
    private LocalDateTime createdAt;
}
