class Subject:
    def __init__(self, subjectId, disease, icd10):
        self.subjectId = subjectId
        self.disease = disease
        self.hasIcd10 = icd10 != None
        self.icd10 = None if not self.hasIcd10 else icd10.replace("ICD10CM:", "")
        self.icdFirstLetter = None if not self.hasIcd10 else self.icd10[0]
        self.isControl = disease == "control"

    def __repr__(self):
        return f"Subject(subjectId={self.subjectId}, disease={self.disease}, icd10={self.icd10} hasIcd10={self.hasIcd10} icdFirstLetter={self.icdFirstLetter} isControl={self.isControl})"
        # return f"Subject(subjectId={self.subjectId}, disease={self.disease}, icd10={self.icd10})"


def get_subjects(session):
    node_count_query = """MATCH (b:Biological_sample)-->(d:Disease)
WITH *, [s in d.synonyms WHERE s STARTS WITH "ICD10CM" | s] as ICD10
RETURN b.subjectid as subjectId, d.name as disease, ICD10[0] as icd10"""     
    data = session.run(node_count_query).data()
    subjects = [Subject(**record) for record in data]
    return subjects