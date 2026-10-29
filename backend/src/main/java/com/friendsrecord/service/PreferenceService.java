package com.friendsrecord.service;

import com.friendsrecord.entity.Preference;
import com.friendsrecord.mapper.PreferenceMapper;
import com.friendsrecord.utils.IdGenerator;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class PreferenceService {

    private final PreferenceMapper preferenceMapper;
    private final FriendService friendService;
    private final AIService aiService;

    public List<Preference> getPreferencesByFriendId(String friendId) {
        return preferenceMapper.findByFriendId(friendId);
    }

    @Transactional
    @CacheEvict(value = "friends", allEntries = true)
    public Preference addPreference(String friendId, Preference preference) {
        // 验证朋友存在
        if (friendService.getFriendById(friendId) == null) {
            throw new RuntimeException("朋友不存在");
        }

        preference.setId(IdGenerator.generate());
        preference.setFriendId(friendId);
        preferenceMapper.insert(preference);

        // 生成向量
        String typeText = "like".equals(preference.getType()) ? "喜好" : "厌恶";
        String text = friendService.getFriendById(friendId).getName() +
                "的" + typeText + ":" + preference.getContent();
        aiService.generateAndStoreVector(preference.getId(), "preference", text);

        return preference;
    }

    @Transactional
    @CacheEvict(value = "friends", allEntries = true)
    public void deletePreference(String friendId, String preferenceId) {
        preferenceMapper.deleteById(preferenceId);
        aiService.deleteVector(preferenceId, "preference");
    }

    @Transactional
    @CacheEvict(value = "friends", allEntries = true)
    public void updatePreferenceTag(String preferenceId, String tag) {
        preferenceMapper.updateTag(preferenceId, tag);
    }
}
