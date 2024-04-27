## Disease names with ICD10 Number

```cypher
MATCH (d:Disease)
WHERE any(s in d.synonyms WHERE s STARTS WITH "ICD10CM")
RETURN d.name
```

## Disease names without ICD10 Number

```cypher
MATCH (d:Disease)
WHERE all(s in d.synonyms WHERE NOT s STARTS WITH "ICD10CM")
RETURN d.name
```

## Healthy Samples

```cypher
MATCH (d:Biological_sample)
WHERE NOT (d)-[:HAS_DISEASE]->()
RETURN d.subjectid
```

## Sick Samples

```cypher
MATCH (d:Biological_sample)
WHERE (d)-[:HAS_DISEASE]->()
RETURN d.subjectid
```