---
topic: Triage Logic: ESI Scale and Resource Allocation
date: 2026-04-21
source: NeoCore Groq Engine
---

# Triage Logic: ESI Scale and Resource Allocation

## Overview

Triage logic is a critical component of emergency medical services (EMS), particularly in high-pressure situations where resources are limited. The Emergency Severity Index (ESI) scale is a widely used triage tool that helps prioritize patients based on the severity of their condition. This entry will outline the ESI scale and its application in resource allocation.

### ESI Scale

The ESI scale is a five-level triage system that categorizes patients based on the urgency of their condition:

1. **Level 1: Resuscitation**: Patients who require immediate life-saving interventions, such as cardiac arrest or severe bleeding.
2. **Level 2: Emergency**: Patients who require prompt treatment, but are not immediately life-threatening, such as severe injuries or acute illnesses.
3. **Level 3: Urgent**: Patients who require treatment within a short period, but are not emergent, such as minor injuries or stable chronic conditions.
4. **Level 4: Semi-Emergent**: Patients who can be treated within a reasonable timeframe, but are not urgent, such as routine check-ups or minor complaints.
5. **Level 5: Non-Emergent**: Patients who do not require immediate medical attention, such as well-child visits or routine vaccinations.

## Concept Map

```markdown
+---------------+
|  Triage Logic  |
+---------------+
       |
       |
       v
+---------------+---------------+
|  ESI Scale    |  Resource Allocation  |
+---------------+---------------+
       |                         |
       |  Level 1: Resuscitation  |  High Priority
       |                         |
       v                         v
+---------------+---------------+---------------+
|  Level 2:     |  Level 3: Urgent  |  Level 4: Semi-  |  Level 5: Non-  |
|  Emergency    |                 |  Emergent       |  Emergent      |
+---------------+---------------+---------------+---------------+
       |                         |                         |
       |  Medium Priority      |  Low Priority        |  Low Priority
       |                         |                         |
       v                         v                         v
+---------------+---------------+---------------+---------------+
|  Treatment   |  Treatment     |  Treatment      |  Treatment    |
|  within 10   |  within 60     |  within 120     |  within 24    |
|  minutes     |  minutes       |  minutes        |  hours        |
+---------------+---------------+---------------+---------------+
```

## References

* [[Emergency Severity Index (ESI)]]
* [[Triage]]
* [[Resource Allocation]]
* [[Emergency Medical Services (EMS)]]