package com.friendsrecord.entity;

import lombok.Data;
import java.io.Serializable;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Data
public class Friend implements Serializable {
    private static final long serialVersionUID = 1L;
    private String id;
    private String name;
    private String gender;
    private LocalDate birthday;
    private String birthdayType; // solar: 阳历, lunar: 农历
    private Integer height;
    private Integer weight;
    private LocalDate knowDate;
    private String occupation;
    private String hometown;
    private String phone;
    private String remark;
    private String avatar;
    private Boolean specialCare;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    // 关联数据
    private List<Preference> preferences;
    private List<Note> notes;
}
