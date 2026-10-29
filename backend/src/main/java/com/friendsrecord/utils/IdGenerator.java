package com.friendsrecord.utils;

import java.util.UUID;

public class IdGenerator {

    public static String generate() {
        return UUID.randomUUID().toString().replace("-", "");
    }

    public static String generateShort() {
        return Long.toHexString(System.currentTimeMillis()) + Integer.toHexString((int)(Math.random() * 10000));
    }
}
