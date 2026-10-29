package com.friendsrecord.mapper;

import com.friendsrecord.entity.Preference;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface PreferenceMapper {

    @Select("SELECT * FROM preferences WHERE friend_id = #{friendId} ORDER BY created_at DESC")
    @Results({
        @Result(property = "id", column = "id"),
        @Result(property = "friendId", column = "friend_id"),
        @Result(property = "type", column = "type"),
        @Result(property = "content", column = "content"),
        @Result(property = "tag", column = "tag"),
        @Result(property = "createdAt", column = "created_at")
    })
    List<Preference> findByFriendId(String friendId);

    @Select("SELECT * FROM preferences WHERE id = #{id}")
    @Results({
        @Result(property = "friendId", column = "friend_id"),
        @Result(property = "createdAt", column = "created_at")
    })
    Preference findById(String id);

    @Insert("INSERT INTO preferences (id, friend_id, type, content, tag, created_at) " +
            "VALUES (#{id}, #{friendId}, #{type}, #{content}, #{tag}, NOW())")
    int insert(Preference preference);

    @Delete("DELETE FROM preferences WHERE id = #{id}")
    int deleteById(String id);

    @Delete("DELETE FROM preferences WHERE friend_id = #{friendId}")
    int deleteByFriendId(String friendId);

    @Update("UPDATE preferences SET tag=#{tag} WHERE id=#{id}")
    int updateTag(@Param("id") String id, @Param("tag") String tag);
}
