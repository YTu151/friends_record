package com.friendsrecord.mapper;

import com.friendsrecord.entity.VectorRecord;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface VectorRecordMapper {

    @Select("SELECT * FROM vector_records WHERE data_type = #{dataType}")
    @Results({
        @Result(property = "id", column = "id"),
        @Result(property = "originalId", column = "original_id"),
        @Result(property = "dataType", column = "data_type"),
        @Result(property = "vectorIndex", column = "vector_index"),
        @Result(property = "content", column = "content"),
        @Result(property = "createdAt", column = "created_at")
    })
    List<VectorRecord> findByDataType(String dataType);

    @Select("SELECT * FROM vector_records WHERE original_id = #{originalId} AND data_type = #{dataType}")
    @Results({
        @Result(property = "originalId", column = "original_id"),
        @Result(property = "dataType", column = "data_type"),
        @Result(property = "vectorIndex", column = "vector_index"),
        @Result(property = "createdAt", column = "created_at")
    })
    VectorRecord findByOriginalIdAndType(@Param("originalId") String originalId, @Param("dataType") String dataType);

    @Insert("INSERT INTO vector_records (id, original_id, data_type, vector_index, content, created_at) " +
            "VALUES (#{id}, #{originalId}, #{dataType}, #{vectorIndex}, #{content}, NOW())")
    int insert(VectorRecord vectorRecord);

    @Delete("DELETE FROM vector_records WHERE original_id = #{originalId} AND data_type = #{dataType}")
    int deleteByOriginalIdAndType(@Param("originalId") String originalId, @Param("dataType") String dataType);

    @Select("SELECT * FROM vector_records")
    @Results({
        @Result(property = "originalId", column = "original_id"),
        @Result(property = "dataType", column = "data_type"),
        @Result(property = "vectorIndex", column = "vector_index"),
        @Result(property = "createdAt", column = "created_at")
    })
    List<VectorRecord> findAll();
}
