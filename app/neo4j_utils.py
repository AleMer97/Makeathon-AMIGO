class Subject:
    def __init__(self, subjectId, name, hasIcd10, isControl):
        self.subjectId = subjectId
        self.name = name
        self.hasIcd10 = hasIcd10
        self.isControl = isControl

    def __repr__(self):
        return f"{self.subjectId} {self.name} {self.hasIcd10} {self.isControl}"


def get_subjects(session):
    node_count_query = """MATCH (b:Biological_sample)-->(d:Disease)
WITH b,d,any(s in d.synonyms WHERE s STARTS WITH "ICD10CM") as hasIcd10
RETURN b.subjectid as subjectId, d.name as name, hasIcd10, d.name = "control" as isControl"""     
    data = session.run(node_count_query).data()
    subjects = [Subject(**record) for record in data]
    return subjects