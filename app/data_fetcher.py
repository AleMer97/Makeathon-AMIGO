class Subject:
    def __init__(self, subjectId, disease, icd10):
        self.subjectId = subjectId
        self.disease = disease
        self.hasIcd10 = icd10 != None
        self.icd10 = None if not self.hasIcd10 else icd10.replace("ICD10CM:", "")
        self.isControl = disease == "control"
        self.isSick = not self.isControl
        self.icdFirstLetter = self.icd10[0] if self.hasIcd10 else ("CTL" if self.isControl else "NC")
        self.phenotypes = []

    def __repr__(self):
        return f"Subject(subjectId={self.subjectId}, disease={self.disease}, icd10={self.icd10})"
    
class ValidationSubject:
    def __init__(self, subjectId):
        self.subjectId = subjectId
        self.phenotypes = []

    def __repr__(self):
        return f"ValidationSubject(subjectId={self.subjectId})"

class Phenotypes:
    def __init__(self, subjectId, phenotypes):
        self.subjectId = subjectId
        self.phenotypes = phenotypes

    def __repr__(self):
        return f"Phenotypes(subjectId={self.subjectId}, phenotypes={self.phenotypes})"
    
def get_phenotypes(session, subjectId):
    query = """MATCH (a:Biological_sample {subjectid:\"""" + subjectId + """\"})-[:HAS_PHENOTYPE]->(p:Phenotype) 
RETURN a.subjectid as subjectId, collect(p.id) as phenotypes"""
    data = session.run(query).data()
    if len(data) == 0:
        return Phenotypes(subjectId=subjectId, phenotypes=[])
    return Phenotypes(**data[0])
    
class DataFetcher:
    def __init__(self, session):
        self.session = session
        self.subjects = self.fetch()
    
    def fetch(self):
        subjects = self.get_subjects(self.session)
        for subject in subjects:
            subject.phenotypes = get_phenotypes(self.session, subject.subjectId).phenotypes
        return subjects

    def get_subjects(self, session):
        query = """MATCH (b:Biological_sample)-->(d:Disease)
    WITH *, [s in d.synonyms WHERE s STARTS WITH "ICD10CM" | s] as ICD10
    RETURN b.subjectid as subjectId, d.name as disease, ICD10[0] as icd10"""     
        data = session.run(query).data()
        subjects = [Subject(**record) for record in data]
        return subjects

class ValidationDataFetcher:
    def __init__(self, session):
        self.session = session
        self.subjects = self.fetch()
    
    def fetch(self):
        subjects = self.get_subjects(self.session)
        for subject in subjects:
            subject.phenotypes = get_phenotypes(self.session, subject.subjectId).phenotypes
        return subjects

    def get_subjects(self, session):
        query = """MATCH (b:Biological_sample)
    WHERE NOT (b)-[:HAS_DISEASE]-(:Disease)
    RETURN b.subjectid as subjectId"""     
        data = session.run(query).data()
        subjects = [ValidationSubject(**record) for record in data]
        return subjects
        