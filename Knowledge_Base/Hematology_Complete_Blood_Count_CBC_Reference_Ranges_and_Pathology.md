---
topic: Hematology: Complete Blood Count (CBC) Reference Ranges and Pathology
date: 2026-04-21
source: NeoCore Groq Engine
---

# Hematology: Complete Blood Count (CBC) Reference Ranges and Pathology

## Overview

A Complete Blood Count (CBC) is a blood test used to evaluate the health of a patient's blood cells, including red blood cells (RBCs), white blood cells (WBCs), and platelets. The CBC is a crucial diagnostic tool in hematology, providing valuable information about various hematological disorders.

## Reference Ranges

| Parameter | Normal Range |
| --- | --- |
| Hemoglobin (Hb) | 13.5-17.5 g/dL |
| Hematocrit (Hct) | 40-54% |
| Red Blood Cell Count (RBC) | 4.32-5.72 x 10^12/L |
| Mean Corpuscular Volume (MCV) | 80-100 fL |
| Mean Corpuscular Hemoglobin (MCH) | 27-31 pg |
| Mean Corpuscular Hemoglobin Concentration (MCHC) | 32-36 g/dL |
| White Blood Cell Count (WBC) | 4.5-11 x 10^9/L |
| Differential Count | |
| - Neutrophils | 45-75% |
| - Lymphocytes | 20-40% |
| - Monocytes | 5-10% |
| - Eosinophils | 1-4% |
| - Basophils | 0-1% |
| Platelet Count (PLT) | 150-450 x 10^9/L |

## Pathology

### Anemia

- **Iron Deficiency Anemia**: Low Hb, low MCV, low MCH
- **Vitamin Deficiency Anemia**: Low Hb, low MCV, low MCH
- **Anemia of Chronic Disease**: Low Hb, low MCV, low MCH
- **Sickle Cell Anemia**: Low Hb, low MCV, abnormal hemoglobin

### Leukemia

- **Acute Lymphoblastic Leukemia (ALL)**: Elevated WBC, abnormal lymphocytes
- **Acute Myeloid Leukemia (AML)**: Elevated WBC, abnormal myeloid cells
- **Chronic Lymphocytic Leukemia (CLL)**: Elevated WBC, abnormal lymphocytes
- **Chronic Myeloid Leukemia (CML)**: Elevated WBC, abnormal myeloid cells

### Thrombocytopenia

- **Idiopathic Thrombocytopenic Purpura (ITP)**: Low PLT
- **Thrombotic Thrombocytopenic Purpura (TTP)**: Low PLT, schistocytes
- **Disseminated Intravascular Coagulation (DIC)**: Low PLT, elevated fibrin degradation products

### Concept Map

```mermaid
graph LR
    A[Anemia] -->|Iron Deficiency|> B[Iron Deficiency Anemia]
    A -->|Vitamin Deficiency|> C[Vitamin Deficiency Anemia]
    A -->|Chronic Disease|> D[Anemia of Chronic Disease]
    A -->|Sickle Cell|> E[Sickle Cell Anemia]
    B -->|Lab Findings|> F[Low Hb, Low MCV, Low MCH]
    C -->|Lab Findings|> F
    D -->|Lab Findings|> F
    E -->|Lab Findings|> G[Abnormal Hemoglobin]
    G -->|Diagnosis|> H[Sickle Cell Anemia]
    A -->|Leukemia|> I[Leukemia]
    I -->|ALL|> J[Acute Lymphoblastic Leukemia]
    I -->|AML|> K[Acute Myeloid Leukemia]
    I -->|CLL|> L[Chronic Lymphocytic Leukemia]
    I -->|CML|> M[Chronic Myeloid Leukemia]
    J -->|Lab Findings|> N[Elevated WBC, Abnormal Lymphocytes]
    K -->|Lab Findings|> N
    L -->|Lab Findings|> N
    M -->|Lab Findings|> N
    N -->|Diagnosis|> O[Leukemia]
    O -->|Thrombocytopenia|> P[Thrombocytopenia]
    P -->|ITP|> Q[Idiopathic Thrombocytopenic Purpura]
    P -->|TTP|> R[Thrombotic Thrombocytopenic Purpura]
    P -->|DIC|> S[Disseminated Intravascular Coagulation]
    Q -->|Lab Findings|> T[Low PLT]
    R -->|Lab Findings|> T
    S -->|Lab Findings|> T
    T -->|Diagnosis|> U[Thrombocytopenia]
```

### References

- [[Hematology]]
- [[Complete Blood Count (CBC)]]
- [[Anemia]]
- [[Leukemia]]
- [[Thrombocytopenia]]