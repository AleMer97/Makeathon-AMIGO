def get_subjectIds(session):
    node_count_query = """MATCH (b:Biological_sample)-->(d:Disease)
WITH b,d,any(s in d.synonyms WHERE s STARTS WITH "ICD10CM") as hasIcd10
RETURN b.subjectid as subjectid, d.name as name, hasIcd10, d.name = "control" as isControl"""     
    return session.run(node_count_query).data()