package com.friendsrecord.mapper;

import com.friendsrecord.entity.ChatHistory;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface ChatHistoryMapper {

    @Select("SELECT * FROM chat_history WHERE session_id = #{sessionId} ORDER BY created_at ASC")
    @Results({
        @Result(property = "id", column = "id"),
        @Result(property = "sessionId", column = "session_id"),
        @Result(property = "role", column = "role"),
        @Result(property = "content", column = "content"),
        @Result(property = "createdAt", column = "created_at")
    })
    List<ChatHistory> findBySessionId(String sessionId);

    @Insert("INSERT INTO chat_history (id, session_id, role, content, created_at) " +
            "VALUES (#{id}, #{sessionId}, #{role}, #{content}, NOW())")
    int insert(ChatHistory chatHistory);

    @Delete("DELETE FROM chat_history WHERE session_id = #{sessionId}")
    int deleteBySessionId(String sessionId);

    @Select("SELECT DISTINCT session_id FROM chat_history ORDER BY MAX(created_at) DESC LIMIT 10")
    List<String> findRecentSessions();
}
