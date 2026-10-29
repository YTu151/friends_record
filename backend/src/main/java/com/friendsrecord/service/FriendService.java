package com.friendsrecord.service;

import com.friendsrecord.entity.Friend;
import com.friendsrecord.mapper.FriendMapper;
import com.friendsrecord.utils.IdGenerator;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class FriendService {

    private final FriendMapper friendMapper;
    private final AIService aiService;

    @Cacheable(value = "friends", key = "'all'")
    public List<Friend> getAllFriends() {
        return friendMapper.findAll();
    }

    @Cacheable(value = "friends", key = "#id")
    public Friend getFriendById(String id) {
        return friendMapper.findById(id);
    }

    @Transactional
    @CacheEvict(value = "friends", allEntries = true)
    public Friend createFriend(Friend friend) {
        friend.setId(IdGenerator.generate());
        friendMapper.insert(friend);

        // 调用AI服务生成向量
        aiService.generateAndStoreVector(friend.getId(), "friend", buildFriendText(friend));

        return friend;
    }

    @Transactional
    @CacheEvict(value = "friends", allEntries = true)
    public Friend updateFriend(String id, Friend friend) {
        friend.setId(id);
        Friend existing = friendMapper.findById(id);
        if (existing != null) {
            // 合并非空字段，避免部分更新覆盖已有数据
            if (friend.getName() == null) friend.setName(existing.getName());
            if (friend.getGender() == null) friend.setGender(existing.getGender());
            if (friend.getBirthday() == null) friend.setBirthday(existing.getBirthday());
            if (friend.getBirthdayType() == null) friend.setBirthdayType(existing.getBirthdayType());
            if (friend.getHeight() == null) friend.setHeight(existing.getHeight());
            if (friend.getWeight() == null) friend.setWeight(existing.getWeight());
            if (friend.getKnowDate() == null) friend.setKnowDate(existing.getKnowDate());
            if (friend.getOccupation() == null) friend.setOccupation(existing.getOccupation());
            if (friend.getHometown() == null) friend.setHometown(existing.getHometown());
            if (friend.getPhone() == null) friend.setPhone(existing.getPhone());
            if (friend.getRemark() == null) friend.setRemark(existing.getRemark());
            if (friend.getAvatar() == null) friend.setAvatar(existing.getAvatar());
            if (friend.getSpecialCare() == null) friend.setSpecialCare(existing.getSpecialCare());
        }
        friendMapper.update(friend);

        // 更新向量
        aiService.generateAndStoreVector(id, "friend", buildFriendText(friend));

        return friendMapper.findById(id);
    }

    @Transactional
    @CacheEvict(value = "friends", allEntries = true)
    public void deleteFriend(String id) {
        friendMapper.deleteById(id);
        // 删除相关向量
        aiService.deleteVector(id, "friend");
    }

    @CacheEvict(value = "friends", allEntries = true)
    public void toggleSpecialCare(String id, Boolean specialCare) {
        friendMapper.updateSpecialCare(id, specialCare);
    }

    @CacheEvict(value = "friends", allEntries = true)
    public void updateAvatar(String id, String avatar) {
        friendMapper.updateAvatar(id, avatar);
    }

    public long getCount() {
        return friendMapper.count();
    }

    private String buildFriendText(Friend friend) {
        StringBuilder sb = new StringBuilder();
        sb.append("姓名:").append(friend.getName()).append(", ");
        sb.append("性别:").append(friend.getGender()).append(", ");
        sb.append("生日:").append(friend.getBirthday()).append(", ");
        sb.append("身高:").append(friend.getHeight()).append("cm, ");
        sb.append("体重:").append(friend.getWeight()).append("kg, ");
        sb.append("职业:").append(friend.getOccupation()).append(", ");
        sb.append("家乡:").append(friend.getHometown()).append(", ");
        sb.append("备注:").append(friend.getRemark());
        return sb.toString();
    }
}
