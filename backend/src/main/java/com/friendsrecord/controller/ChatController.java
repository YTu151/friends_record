package com.friendsrecord.controller;

import com.friendsrecord.entity.ChatHistory;
import com.friendsrecord.service.ChatService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/chat")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class ChatController {

    private final ChatService chatService;

    @GetMapping("/history")
    public ResponseEntity<List<ChatHistory>> getChatHistory(@RequestParam String sessionId) {
        return ResponseEntity.ok(chatService.getChatHistory(sessionId));
    }

    @PostMapping("/send")
    public ResponseEntity<Map<String, String>> sendMessage(@RequestBody Map<String, String> request) {
        String sessionId = request.get("sessionId");
        String message = request.get("message");

        String response = chatService.sendMessage(sessionId, message);

        Map<String, String> result = new HashMap<>();
        result.put("response", response);
        return ResponseEntity.ok(result);
    }

    @DeleteMapping("/history")
    public ResponseEntity<Void> clearHistory(@RequestParam String sessionId) {
        chatService.clearHistory(sessionId);
        return ResponseEntity.ok().build();
    }
}
