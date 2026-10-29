package com.friendsrecord.service;

import com.friendsrecord.entity.ChatHistory;
import com.friendsrecord.mapper.ChatHistoryMapper;
import com.friendsrecord.utils.IdGenerator;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.hc.client5.http.classic.methods.HttpPost;
import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.CloseableHttpResponse;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.core5.http.io.entity.EntityUtils;
import org.apache.hc.core5.http.io.entity.StringEntity;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Service
@RequiredArgsConstructor
public class ChatService {

    private final ChatHistoryMapper chatHistoryMapper;

    @Value("${ai.service.url:http://localhost:8000}")
    private String aiServiceUrl;

    public List<ChatHistory> getChatHistory(String sessionId) {
        return chatHistoryMapper.findBySessionId(sessionId);
    }

    public String sendMessage(String sessionId, String message) {
        try {
            // 1. 保存用户消息
            ChatHistory userMsg = new ChatHistory();
            userMsg.setId(IdGenerator.generate());
            userMsg.setSessionId(sessionId);
            userMsg.setRole("user");
            userMsg.setContent(message);
            chatHistoryMapper.insert(userMsg);

            // 2. 调用Python AI服务
            String aiResponse = callAIService(sessionId, message);

            // 3. 保存AI响应
            ChatHistory aiMsg = new ChatHistory();
            aiMsg.setId(IdGenerator.generate());
            aiMsg.setSessionId(sessionId);
            aiMsg.setRole("assistant");
            aiMsg.setContent(aiResponse);
            chatHistoryMapper.insert(aiMsg);

            return aiResponse;
        } catch (Exception e) {
            log.error("发送消息失败", e);
            return "抱歉，AI服务暂时不可用，请稍后重试。";
        }
    }

    public void clearHistory(String sessionId) {
        chatHistoryMapper.deleteBySessionId(sessionId);
    }

    private String callAIService(String sessionId, String message) {
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpPost httpPost = new HttpPost(aiServiceUrl + "/chat");
            httpPost.setHeader("Content-Type", "application/json");

            Map<String, String> requestBody = new HashMap<>();
            requestBody.put("session_id", sessionId);
            requestBody.put("message", message);

            String jsonBody = com.alibaba.fastjson2.JSON.toJSONString(requestBody);
            httpPost.setEntity(new StringEntity(jsonBody, StandardCharsets.UTF_8));

            try (CloseableHttpResponse response = httpClient.execute(httpPost)) {
                String responseBody = EntityUtils.toString(response.getEntity(), StandardCharsets.UTF_8);
                Map<String, Object> result = com.alibaba.fastjson2.JSON.parseObject(responseBody, Map.class);
                return (String) result.getOrDefault("response", "AI无响应");
            }
        } catch (Exception e) {
            log.error("调用AI服务失败", e);
            return "AI服务调用失败: " + e.getMessage();
        }
    }
}
