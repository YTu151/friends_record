package com.friendsrecord.mapper;

import com.friendsrecord.entity.Note;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface NoteMapper {

    @Select("SELECT n.*, f.name as friend_name FROM notes n " +
            "LEFT JOIN friends f ON n.friend_id = f.id " +
            "ORDER BY n.created_at DESC")
    @Results({
        @Result(property = "id", column = "id"),
        @Result(property = "friendId", column = "friend_id"),
        @Result(property = "title", column = "title"),
        @Result(property = "content", column = "content"),
        @Result(property = "noteTime", column = "note_time"),
        @Result(property = "createdAt", column = "created_at"),
        @Result(property = "updatedAt", column = "updated_at"),
        @Result(property = "friendName", column = "friend_name")
    })
    List<Note> findAll();

    @Select("SELECT * FROM notes WHERE friend_id = #{friendId} ORDER BY created_at DESC")
    @Results({
        @Result(property = "friendId", column = "friend_id"),
        @Result(property = "noteTime", column = "note_time"),
        @Result(property = "createdAt", column = "created_at"),
        @Result(property = "updatedAt", column = "updated_at")
    })
    List<Note> findByFriendId(String friendId);

    @Select("SELECT n.*, f.name as friend_name FROM notes n " +
            "LEFT JOIN friends f ON n.friend_id = f.id " +
            "WHERE n.id = #{id}")
    @Results({
        @Result(property = "friendId", column = "friend_id"),
        @Result(property = "noteTime", column = "note_time"),
        @Result(property = "createdAt", column = "created_at"),
        @Result(property = "updatedAt", column = "updated_at"),
        @Result(property = "friendName", column = "friend_name")
    })
    Note findById(String id);

    @Insert("INSERT INTO notes (id, friend_id, title, content, note_time, created_at, updated_at) " +
            "VALUES (#{id}, #{friendId}, #{title}, #{content}, #{noteTime}, NOW(), NOW())")
    int insert(Note note);

    @Update("UPDATE notes SET friend_id=#{friendId}, title=#{title}, content=#{content}, " +
            "note_time=#{noteTime}, updated_at=NOW() WHERE id=#{id}")
    int update(Note note);

    @Delete("DELETE FROM notes WHERE id = #{id}")
    int deleteById(String id);

    @Select("SELECT COUNT(*) FROM notes")
    long count();
}
