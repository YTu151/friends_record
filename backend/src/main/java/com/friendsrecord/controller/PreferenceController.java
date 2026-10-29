package com.friendsrecord.controller;

import com.friendsrecord.entity.Preference;
import com.friendsrecord.service.PreferenceService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/friends/{friendId}/preferences")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class PreferenceController {

    private final PreferenceService preferenceService;

    @GetMapping
    public ResponseEntity<List<Preference>> getPreferences(@PathVariable String friendId) {
        return ResponseEntity.ok(preferenceService.getPreferencesByFriendId(friendId));
    }

    @PostMapping
    public ResponseEntity<Preference> addPreference(
            @PathVariable String friendId,
            @RequestBody Preference preference) {
        return ResponseEntity.ok(preferenceService.addPreference(friendId, preference));
    }

    @DeleteMapping("/{preferenceId}")
    public ResponseEntity<Void> deletePreference(
            @PathVariable String friendId,
            @PathVariable String preferenceId) {
        preferenceService.deletePreference(friendId, preferenceId);
        return ResponseEntity.ok().build();
    }

    @PutMapping("/{preferenceId}/tag")
    public ResponseEntity<Void> updatePreferenceTag(
            @PathVariable String friendId,
            @PathVariable String preferenceId,
            @RequestBody Map<String, String> body) {
        preferenceService.updatePreferenceTag(preferenceId, body.get("tag"));
        return ResponseEntity.ok().build();
    }
}
