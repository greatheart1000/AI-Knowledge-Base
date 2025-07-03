from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_relationship(self, start_entity, relationship_type, end_entity, relationship_summary):
        with self.driver.session() as session:
            session.write_transaction(
                self._create_and_return_relationship,
                start_entity,
                relationship_type,
                end_entity,
                relationship_summary
            )

    @staticmethod
    def _create_and_return_relationship(tx, start_entity, relationship_type, end_entity, relationship_summary):
        query = (
            "MATCH (a:Entity {name: $start_entity}), (b:Entity {name: $end_entity}) "
            "MERGE (a)-[r:RELATES_TO {type: $relationship_type, summary: $relationship_summary}]->(b)"
        )
        tx.run(query, start_entity=start_entity, relationship_type=relationship_type, end_entity=end_entity, relationship_summary=relationship_summary)

if __name__ == "__main__":
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "123456"  # 替换为您的密码

    neo4j_handler = Neo4jHandler(uri, user, password)

    # 示例关系数据
    relationships = [
        ("菲尔・贾伯", "创建", "菲尔兹咖啡", "1978年在加利福尼亚州伯克利创立"),
        ("菲尔兹咖啡", "位于", "加利福尼亚州伯克利", "菲尔兹咖啡的创立地点"),
        ("菲尔・贾伯", "拥有", "雅各布・贾伯", "菲尔・贾伯的大儿子"),
        ("雅各布・贾伯", "管理", "菲尔兹咖啡", "在2005年担任首席执行官"),
        ("菲尔兹咖啡", "扩展至", "美国多地", "菲尔兹咖啡的扩展范围"),
    ]

    for start_entity, relationship_type, end_entity, relationship_summary in relationships:
        neo4j_handler.create_relationship(start_entity, relationship_type, end_entity, relationship_summary)

    neo4j_handler.close()

"""查询示例
您可以使用以下 Cypher 查询查看存储的关系及其属性：
MATCH (a)-[r:RELATES_TO]->(b) RETURN a, r, b
"""