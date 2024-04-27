class Subject:
    def __init__(self, subjectId, disease, icd10):
        self.subjectId = subjectId
        self.disease = disease
        self.icd10 = icd10
        self.hasIcd10 = icd10 != None
        self.isControl = disease == "Control"

    def __repr__(self):
        return f"Subject(subjectId={self.subjectId}, disease={self.disease}, icd10={self.icd10})"


def get_subjects(session):
    node_count_query = """MATCH (b:Biological_sample)-->(d:Disease)
WITH *, [s in d.synonyms WHERE s STARTS WITH "ICD10CM" | s] as ICD10
RETURN b.subjectid as subjectId, d.name as disease, ICD10[0]"""     
    data = session.run(node_count_query).data()
    subjects = [Subject(**record) for record in data]
    return subjects