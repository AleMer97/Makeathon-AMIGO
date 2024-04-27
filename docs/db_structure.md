## Protein

- IN

```
(p:Peptide)-[b BELONGS_TO_PROTEIN]->(P:Protein)
(g:Gene)-[t:TRANSCRIBED_INTO]->(m:Transcript)-[T:TRANSLATED_INTO]->(P:Protein)
```

- OUT

```
(P:Protein)-[d:DETECTED_IN_PATHOLOGY_SAMPLE]->(d:Disease)
```

## Biological_sample

- OUT

```
(b:Biological_sample)-[b:BELONGS_TO_SUBJECT]->(s:Subject)
(b:Biological_sample)-[h:HAS_DISEASE]->(d:Disease)
(b:Biological_sample)-[h:HAS_DAMAGE]->(d:Gene)
(b:Biological_sample)-[h:HAS_PROTEIN]->(p:Protein)
(b:Biological_sample)-[h:HAS_PHENOTYPE]->(p:Phenotype)
```

- Transcript: MRNA
