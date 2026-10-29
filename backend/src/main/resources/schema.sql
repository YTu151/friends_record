-- 朋友信息表
CREATE TABLE IF NOT EXISTS friends (
    id VARCHAR(32) PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    gender VARCHAR(10) COMMENT '性别',
    birthday DATE COMMENT '生日',
    birthday_type VARCHAR(10) DEFAULT 'solar' COMMENT '生日类型：solar阳历，lunar农历',
    height INT COMMENT '身高(cm)',
    weight INT COMMENT '体重(kg)',
    know_date DATE COMMENT '认识时间',
    occupation VARCHAR(100) COMMENT '职业',
    hometown VARCHAR(100) COMMENT '家乡',
    phone VARCHAR(20) COMMENT '联系方式',
    remark TEXT COMMENT '备注',
    avatar VARCHAR(500) COMMENT '头像URL',
    special_care TINYINT(1) DEFAULT 0 COMMENT '特别关心',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_name (name),
    INDEX idx_birthday (birthday)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='朋友信息表';

-- 偏好喜好表
CREATE TABLE IF NOT EXISTS preferences (
    id VARCHAR(32) PRIMARY KEY,
    friend_id VARCHAR(32) NOT NULL COMMENT '朋友ID',
    type VARCHAR(20) NOT NULL COMMENT '类型：like喜好，dislike厌恶',
    content VARCHAR(500) NOT NULL COMMENT '内容',
    tag VARCHAR(50) COMMENT '标签',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (friend_id) REFERENCES friends(id) ON DELETE CASCADE,
    INDEX idx_friend_id (friend_id),
    INDEX idx_type (type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='偏好喜好表';

-- 便签记录表
CREATE TABLE IF NOT EXISTS notes (
    id VARCHAR(32) PRIMARY KEY,
    friend_id VARCHAR(32) NOT NULL COMMENT '朋友ID',
    title VARCHAR(200) COMMENT '标题',
    content TEXT NOT NULL COMMENT '内容',
    note_time DATETIME COMMENT '记录时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (friend_id) REFERENCES friends(id) ON DELETE CASCADE,
    INDEX idx_friend_id (friend_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='便签记录表';

-- AI对话历史表
CREATE TABLE IF NOT EXISTS chat_history (
    id VARCHAR(32) PRIMARY KEY,
    session_id VARCHAR(64) NOT NULL COMMENT '会话ID',
    role VARCHAR(20) NOT NULL COMMENT '角色：user用户，assistant助手',
    content TEXT NOT NULL COMMENT '内容',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_session_id (session_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI对话历史表';

-- 向量关联记录表
CREATE TABLE IF NOT EXISTS vector_records (
    id VARCHAR(32) PRIMARY KEY,
    original_id VARCHAR(32) NOT NULL COMMENT '原始数据ID',
    data_type VARCHAR(20) NOT NULL COMMENT '数据类型：friend朋友，preference偏好，note便签',
    vector_index VARCHAR(100) COMMENT '向量存储索引',
    content TEXT COMMENT '原始文本内容',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_original_type (original_id, data_type),
    INDEX idx_data_type (data_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='向量关联记录表';
