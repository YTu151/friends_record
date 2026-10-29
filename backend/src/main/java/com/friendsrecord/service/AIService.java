package com.friendsrecord.service;

import com.friendsrecord.mapper.VectorRecordMapper;
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
import java.util.Map;

@Slf4j
@Service
@RequiredArgsConstructor
public class AIService {

    @Value("${ai.service.url:http://localhost:8000}")
    private String aiServiceUrl;

    private final VectorRecordMapper vectorRecordMapper;

    public void generateAndStoreVector(String originalId, String dataType, String content) {
        try {
            Map<String, String> request = new HashMap<>();
            request.put("original_id", originalId);
            request.put("data_type", dataType);
            request.put("content", content);

            String jsonBody = com.alibaba.fastjson2.JSON.toJSONString(request);

            try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
                HttpPost httpPost = new HttpPost(aiServiceUrl + "/vector/embed");
                httpPost.setHeader("Content-Type", "application/json");
                httpPost.setEntity(new StringEntity(jsonBody, StandardCharsets.UTF_8));

                try (CloseableHttpResponse response = httpClient.execute(httpPost)) {
                    String responseBody = EntityUtils.toString(response.getEntity(), StandardCharsets.UTF_8);
                    log.info("向量生成结果: {}", responseBody);
                }
            }
        } catch (Exception e) {
            log.error("生成向量失败", e);
        }
    }

    public void deleteVector(String originalId, String dataType) {
        try {
            try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
                HttpPost httpPost = new HttpPost(aiServiceUrl + "/vector/delete");
                httpPost.setHeader("Content-Type", "application/json");

                Map<String, String> request = new HashMap<>();
                request.put("original_id", originalId);
                request.put("data_type", dataType);

                String jsonBody = com.alibaba.fastjson2.JSON.toJSONString(request);
                httpPost.setEntity(new StringEntity(jsonBody, StandardCharsets.UTF_8));

                httpClient.execute(httpPost).close();
            }
        } catch (Exception e) {
            log.error("删除向量失败", e);
        }
    }
}
