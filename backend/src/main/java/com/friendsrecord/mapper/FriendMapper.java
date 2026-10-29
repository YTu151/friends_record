package com.friendsrecord.mapper;

import com.friendsrecord.entity.Friend;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface FriendMapper {

    @Select("SELECT * FROM friends ORDER BY created_at DESC")
    @Results({
        @Result(property = "id", column = "id"),
        @Result(property = "name", column = "name"),
        @Result(property = "gender", column = "gender"),
        @Result(property = "birthday", column = "birthday"),
        @Result(property = "birthdayType", column = "birthday_type"),
        @Result(property = "height", column = "height"),
        @Result(property = "weight", column = "weight"),
        @Result(property = "knowDate", column = "know_date"),
        @Result(property = "occupation", column = "occupation"),
        @Result(property = "hometown", column = "hometown"),
        @Result(property = "phone", column = "phone"),
        @Result(property = "remark", column = "remark"),
        @Result(property = "avatar", column = "avatar"),
        @Result(property = "specialCare", column = "special_care"),
        @Result(property = "createdAt", column = "created_at"),
        @Result(property = "updatedAt", column = "updated_at"),
        @Result(property = "preferences", column = "id",
                many = @Many(select = "com.friendsrecord.mapper.PreferenceMapper.findByFriendId")),
        @Result(property = "notes", column = "id",
                many = @Many(select = "com.friendsrecord.mapper.NoteMapper.findByFriendId"))
    })
    List<Friend> findAll();

    @Select("SELECT * FROM friends WHERE id = #{id}")
    @Results({
        @Result(property = "id", column = "id"),
        @Result(property = "birthdayType", column = "birthday_type"),
        @Result(property = "knowDate", column = "know_date"),
        @Result(property = "avatar", column = "avatar"),
        @Result(property = "specialCare", column = "special_care"),
        @Result(property = "createdAt", column = "created_at"),
        @Result(property = "updatedAt", column = "updated_at"),
        @Result(property = "preferences", column = "id",
                many = @Many(select = "com.friendsrecord.mapper.PreferenceMapper.findByFriendId")),
        @Result(property = "notes", column = "id",
                many = @Many(select = "com.friendsrecord.mapper.NoteMapper.findByFriendId"))
    })
    Friend findById(String id);

    @Insert("INSERT INTO friends (id, name, gender, birthday, birthday_type, height, weight, " +
            "know_date, occupation, hometown, phone, remark, avatar, special_care, created_at, updated_at) " +
            "VALUES (#{id}, #{name}, #{gender}, #{birthday}, #{birthdayType}, #{height}, #{weight}, " +
            "#{knowDate}, #{occupation}, #{hometown}, #{phone}, #{remark}, #{avatar}, #{specialCare}, NOW(), NOW())")
    int insert(Friend friend);

    @Update("UPDATE friends SET name=#{name}, gender=#{gender}, birthday=#{birthday}, " +
            "birthday_type=#{birthdayType}, height=#{height}, weight=#{weight}, " +
            "know_date=#{knowDate}, occupation=#{occupation}, hometown=#{hometown}, " +
            "phone=#{phone}, remark=#{remark}, avatar=#{avatar}, special_care=#{specialCare}, updated_at=NOW() WHERE id=#{id}")
    int update(Friend friend);

    @Update("UPDATE friends SET special_care=#{specialCare}, updated_at=NOW() WHERE id=#{id}")
    int updateSpecialCare(@Param("id") String id, @Param("specialCare") Boolean specialCare);

    @Update("UPDATE friends SET avatar=#{avatar}, updated_at=NOW() WHERE id=#{id}")
    int updateAvatar(@Param("id") String id, @Param("avatar") String avatar);

    @Delete("DELETE FROM friends WHERE id = #{id}")
    int deleteById(String id);

    @Select("SELECT COUNT(*) FROM friends")
    long count();
}
