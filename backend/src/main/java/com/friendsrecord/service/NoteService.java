package com.friendsrecord.service;

import com.friendsrecord.entity.Note;
import com.friendsrecord.mapper.NoteMapper;
import com.friendsrecord.utils.IdGenerator;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@RequiredArgsConstructor
public class NoteService {

    private final NoteMapper noteMapper;
    private final FriendService friendService;
    private final AIService aiService;

    @Cacheable(value = "notes", key = "'all'")
    public List<Note> getAllNotes() {
        return noteMapper.findAll();
    }

    public List<Note> getNotesByFriendId(String friendId) {
        return noteMapper.findByFriendId(friendId);
    }

    @Cacheable(value = "notes", key = "#id")
    public Note getNoteById(String id) {
        return noteMapper.findById(id);
    }

    @Transactional
    @CacheEvict(value = "notes", allEntries = true)
    public Note createNote(Note note) {
        // 验证朋友存在
        if (friendService.getFriendById(note.getFriendId()) == null) {
            throw new RuntimeException("朋友不存在");
        }

        note.setId(IdGenerator.generate());
        noteMapper.insert(note);

        // 生成向量
        String friendName = friendService.getFriendById(note.getFriendId()).getName();
        String text = "关于" + friendName + "的便签:" + note.getContent();
        aiService.generateAndStoreVector(note.getId(), "note", text);

        return note;
    }

    @Transactional
    @CacheEvict(value = "notes", allEntries = true)
    public Note updateNote(String id, Note note) {
        note.setId(id);
        noteMapper.update(note);

        // 更新向量
        String friendName = friendService.getFriendById(note.getFriendId()).getName();
        String text = "关于" + friendName + "的便签:" + note.getContent();
        aiService.generateAndStoreVector(id, "note", text);

        return noteMapper.findById(id);
    }

    @Transactional
    @CacheEvict(value = "notes", allEntries = true)
    public void deleteNote(String id) {
        noteMapper.deleteById(id);
        aiService.deleteVector(id, "note");
    }

    public long getCount() {
        return noteMapper.count();
    }
}
