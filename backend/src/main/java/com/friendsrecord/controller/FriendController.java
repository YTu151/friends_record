package com.friendsrecord.controller;

import com.friendsrecord.entity.Friend;
import com.friendsrecord.service.FriendService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/friends")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class FriendController {

    private final FriendService friendService;

    @GetMapping
    public ResponseEntity<List<Friend>> getAllFriends() {
        return ResponseEntity.ok(friendService.getAllFriends());
    }

    @GetMapping("/{id}")
    public ResponseEntity<Friend> getFriendById(@PathVariable String id) {
        Friend friend = friendService.getFriendById(id);
        if (friend == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(friend);
    }

    @PostMapping
    public ResponseEntity<Friend> createFriend(@RequestBody Friend friend) {
        return ResponseEntity.ok(friendService.createFriend(friend));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Friend> updateFriend(@PathVariable String id, @RequestBody Friend friend) {
        return ResponseEntity.ok(friendService.updateFriend(id, friend));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteFriend(@PathVariable String id) {
        friendService.deleteFriend(id);
        return ResponseEntity.ok().build();
    }

    @PutMapping("/{id}/special-care")
    public ResponseEntity<Void> toggleSpecialCare(@PathVariable String id, @RequestBody Map<String, Boolean> body) {
        friendService.toggleSpecialCare(id, body.getOrDefault("specialCare", false));
        return ResponseEntity.ok().build();
    }

    @PutMapping("/{id}/avatar")
    public ResponseEntity<Void> updateAvatar(@PathVariable String id, @RequestBody Map<String, String> body) {
        friendService.updateAvatar(id, body.get("avatar"));
        return ResponseEntity.ok().build();
    }

    @GetMapping("/stats")
    public ResponseEntity<Map<String, Long>> getStats() {
        Map<String, Long> stats = new HashMap<>();
        stats.put("count", friendService.getCount());
        return ResponseEntity.ok(stats);
    }
}
