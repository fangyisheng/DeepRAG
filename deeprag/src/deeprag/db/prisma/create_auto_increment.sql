-- 创建序列并设置默认值
-- 1. knowledge_space 表的 human_readable_id 序列
CREATE SEQUENCE knowledge_space_human_readable_id_seq START WITH 1 INCREMENT BY 1;
ALTER TABLE "knowledge_space"
ALTER COLUMN "human_readable_id"
SET DEFAULT nextval('knowledge_space_human_readable_id_seq');
-- 2. file 表的 human_readable_id 序列
CREATE SEQUENCE file_human_readable_id_seq START WITH 1 INCREMENT BY 1;
ALTER TABLE "file"
ALTER COLUMN "human_readable_id"
SET DEFAULT nextval('file_human_readable_id_seq');
-- 3. text_chunk 表的 human_readable_id 序列
CREATE SEQUENCE text_chunk_human_readable_id_seq START WITH 1 INCREMENT BY 1;
ALTER TABLE "text_chunk"
ALTER COLUMN "human_readable_id"
SET DEFAULT nextval('text_chunk_human_readable_id_seq');
-- 4. sub_graph_data 表的 human_readable_id 序列
CREATE SEQUENCE sub_graph_data_human_readable_id_seq START WITH 1 INCREMENT BY 1;
ALTER TABLE "sub_graph_data"
ALTER COLUMN "human_readable_id"
SET DEFAULT nextval('sub_graph_data_human_readable_id_seq');
-- 5. merged_graph_data 表的 human_readable_id 序列
CREATE SEQUENCE merged_graph_data_human_readable_id_seq START WITH 1 INCREMENT BY 1;
ALTER TABLE "merged_graph_data"
ALTER COLUMN "human_readable_id"
SET DEFAULT nextval('merged_graph_data_human_readable_id_seq');
-- 6. flatten_entity_relation 表的 human_readable_id 序列
CREATE SEQUENCE flatten_entity_relation_human_readable_id_seq START WITH 1 INCREMENT BY 1;
ALTER TABLE "flatten_entity_relation"
ALTER COLUMN "human_readable_id"
SET DEFAULT nextval('flatten_entity_relation_human_readable_id_seq');
-- 7. community_cluster 表的 human_readable_id 序列
CREATE SEQUENCE community_cluster_human_readable_id_seq START WITH 1 INCREMENT BY 1;
ALTER TABLE "community_cluster"
ALTER COLUMN "human_readable_id"
SET DEFAULT nextval('community_cluster_human_readable_id_seq');
-- 8. community_report 表的 human_readable_id 序列
CREATE SEQUENCE community_report_human_readable_id_seq START WITH 1 INCREMENT BY 1;
ALTER TABLE "community_report"
ALTER COLUMN "human_readable_id"
SET DEFAULT nextval('community_report_human_readable_id_seq');
-- 9. user 表的 human_readable_id 序列
CREATE SEQUENCE user_human_readable_id_seq START WITH 1 INCREMENT BY 1;
ALTER TABLE "user"
ALTER COLUMN "human_readable_id"
SET DEFAULT nextval('user_human_readable_id_seq');
-- 10. llm_chat 表的 human_readable_id 序列
CREATE SEQUENCE llm_chat_human_readable_id_seq START WITH 1 INCREMENT BY 1;
ALTER TABLE "llm_chat"
ALTER COLUMN "human_readable_id"
SET DEFAULT nextval('llm_chat_human_readable_id_seq');
-- 11. rag_param 表的 human_readable_id 序列
CREATE SEQUENCE rag_param_human_readable_id_seq START WITH 1 INCREMENT BY 1;
ALTER TABLE "rag_param"
ALTER COLUMN "human_readable_id"
SET DEFAULT nextval('rag_param_human_readable_id_seq');